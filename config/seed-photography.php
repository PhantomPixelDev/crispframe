<?php
declare(strict_types=1);

// Development/export helper. Attach starter photographs only to untouched demo heroes.
$loader = require dirname(__DIR__) . '/vendor/autoload.php';
\TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::run(0, \TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::REQUESTTYPE_CLI);
\TYPO3\CMS\Core\Core\Bootstrap::init($loader);
\TYPO3\CMS\Core\Core\Bootstrap::initializeBackendUser(\TYPO3\CMS\Core\Authentication\CommandLineUserAuthentication::class);
\TYPO3\CMS\Core\Core\Bootstrap::initializeBackendAuthentication();

$pool = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\TYPO3\CMS\Core\Database\ConnectionPool::class);
$content = $pool->getConnectionForTable('tt_content');
$refs = $pool->getConnectionForTable('sys_file_reference');
$factory = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\TYPO3\CMS\Core\Resource\ResourceFactory::class);
$storage = $factory->getDefaultStorage();
$parent = $storage->getFolder('user_upload/');
$folder = $storage->hasFolder('user_upload/crispframe-demo/')
    ? $storage->getFolder('user_upload/crispframe-demo/')
    : $storage->createFolder('crispframe-demo', $parent);
$definitions = [
    'Demo: home hero' => [
        'file' => 'studio-team.webp',
        'en' => 'A team reviews ideas together at a bright studio table',
        'de' => 'Ein Team bespricht Ideen an einem hellen Studiotisch',
    ],
    'Demo: work hero' => [
        'file' => 'project-worktable.webp',
        'en' => 'Printed project concepts and materials arranged on a worktable',
        'de' => 'Gedruckte Projektentwürfe und Materialien auf einem Arbeitstisch',
    ],
    'Demo: contact hero' => [
        'file' => 'meeting-space.webp',
        'en' => 'A welcoming sunlit meeting space with a round table',
        'de' => 'Ein einladender, sonniger Besprechungsraum mit rundem Tisch',
    ],
];
foreach ($definitions as $marker => $definition) {
    $file = $storage->addFile(
        dirname(__DIR__) . '/packages/agency_demo/Resources/Public/Images/' . $definition['file'],
        $folder,
        $definition['file'],
        \TYPO3\CMS\Core\Resource\DuplicationBehavior::REPLACE,
        false
    );
    $sourceReference = 0;
    foreach ($content->fetchAllAssociative(
        "SELECT uid, pid, sys_language_uid, crispframe_hero_image, crispframe_hero_imageAlt FROM tt_content WHERE CType = 'crispframe_hero' AND header = ? AND deleted = 0 ORDER BY sys_language_uid ASC",
        [$marker]
    ) as $hero) {
        $uid = (int)$hero['uid'];
        $language = (int)$hero['sys_language_uid'];
        $reference = $refs->fetchAssociative(
            "SELECT uid, uid_local FROM sys_file_reference WHERE tablenames = 'tt_content' AND fieldname = 'crispframe_hero_image' AND uid_foreign = ? AND deleted = 0",
            [$uid]
        );
        if ($reference) {
            if ((int)$reference['uid_local'] === $file->getUid()) {
                if ($language === 0) {
                    $sourceReference = (int)$reference['uid'];
                } elseif ($language === 1 && $sourceReference > 0) {
                    $refs->update('sys_file_reference', ['sys_language_uid' => 1, 'l10n_parent' => $sourceReference], ['uid' => (int)$reference['uid']]);
                }
            }
            continue;
        }
        if ((int)$hero['crispframe_hero_image'] !== 0) {
            continue;
        }
        $alt = $language === 1 ? $definition['de'] : $definition['en'];
        $refs->insert('sys_file_reference', [
            'pid' => (int)$hero['pid'], 'uid_local' => $file->getUid(), 'uid_foreign' => $uid,
            'tablenames' => 'tt_content', 'fieldname' => 'crispframe_hero_image',
            'sorting_foreign' => 1, 'hidden' => 0, 'alternative' => $alt,
            'sys_language_uid' => $language, 'l10n_parent' => $language === 1 ? $sourceReference : 0,
        ]);
        if ($language === 0) {
            $sourceReference = (int)$refs->lastInsertId();
        }
        $update = ['crispframe_hero_image' => 1];
        if ($hero['crispframe_hero_imageAlt'] === '') {
            $update['crispframe_hero_imageAlt'] = $alt;
        }
        $content->update('tt_content', $update, ['uid' => $uid]);
    }
}
echo "Demo photography ready.\n";
