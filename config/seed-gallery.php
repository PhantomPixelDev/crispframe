<?php
declare(strict_types=1);

// Repeatable local-only gallery demo. Run after extension:setup.
$loader = require dirname(__DIR__) . '/vendor/autoload.php';
\TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::run(0, \TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::REQUESTTYPE_CLI);
\TYPO3\CMS\Core\Core\Bootstrap::init($loader);
\TYPO3\CMS\Core\Core\Bootstrap::initializeBackendUser(\TYPO3\CMS\Core\Authentication\CommandLineUserAuthentication::class);
\TYPO3\CMS\Core\Core\Bootstrap::initializeBackendAuthentication();

$pool = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\TYPO3\CMS\Core\Database\ConnectionPool::class);
$pages = $pool->getConnectionForTable('pages');
$content = $pool->getConnectionForTable('tt_content');
$items = $pool->getConnectionForTable('crispframe_gallery_items');
$refs = $pool->getConnectionForTable('sys_file_reference');
$page = (int)$pages->fetchOne("SELECT uid FROM pages WHERE slug = '/components' AND deleted = 0");
if (!$page) {
    throw new RuntimeException('Run config/seed-demo.php first.');
}
$marker = 'Demo: gallery';
$block = (int)$content->fetchOne('SELECT uid FROM tt_content WHERE pid = ? AND header = ? AND deleted = 0', [$page, $marker]);
if (!$block) {
    $content->insert('tt_content', [
        'pid' => $page, 'CType' => 'crispframe_gallery', 'header' => $marker,
        'colPos' => 0, 'sorting' => 384, 'hidden' => 0,
        'crispframe_gallery_headline' => 'A gallery for real project imagery',
        'crispframe_gallery_lead' => 'Each image can have its own caption and alternative text.',
        'crispframe_gallery_sectionBackground' => 'subtle',
        'crispframe_gallery_sectionSpacing' => 'default',
        'crispframe_gallery_width' => 'default',
    ]);
    $block = (int)$content->lastInsertId();
}

$factory = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\TYPO3\CMS\Core\Resource\ResourceFactory::class);
$storage = $factory->getDefaultStorage();
$parent = $storage->getFolder('user_upload/');
$folder = $storage->hasFolder('user_upload/crispframe-demo/')
    ? $storage->getFolder('user_upload/crispframe-demo/')
    : $storage->createFolder('crispframe-demo', $parent);
$definitions = [
    ['file' => 'workspace.svg', 'caption' => 'A clear workspace', 'alt' => 'Abstract blue interface illustration'],
    ['file' => 'collaboration.svg', 'caption' => 'Ideas in motion', 'alt' => 'Abstract green collaboration illustration'],
];
foreach ($definitions as $index => $definition) {
    $file = $storage->addFile(
        dirname(__DIR__) . '/packages/agency_demo/Resources/Public/Images/' . $definition['file'],
        $folder,
        $definition['file'],
        \TYPO3\CMS\Core\Resource\DuplicationBehavior::REPLACE,
        false
    );
    $item = (int)$items->fetchOne('SELECT uid FROM crispframe_gallery_items WHERE foreign_table_parent_uid = ? AND caption = ? AND deleted = 0', [$block, $definition['caption']]);
    if (!$item) {
        $items->insert('crispframe_gallery_items', [
            'pid' => $page, 'foreign_table_parent_uid' => $block,
            'sorting' => ($index + 1) * 128, 'hidden' => 0,
            'caption' => $definition['caption'], 'image' => 1,
        ]);
        $item = (int)$items->lastInsertId();
    }
    if (!$refs->fetchOne("SELECT uid FROM sys_file_reference WHERE tablenames = 'crispframe_gallery_items' AND fieldname = 'image' AND uid_foreign = ? AND deleted = 0", [$item])) {
        $refs->insert('sys_file_reference', [
            'pid' => $page, 'uid_local' => $file->getUid(), 'uid_foreign' => $item,
            'tablenames' => 'crispframe_gallery_items', 'fieldname' => 'image',
            'sorting_foreign' => 1, 'hidden' => 0, 'alternative' => $definition['alt'],
        ]);
    }
}
$count = (int)$items->fetchOne('SELECT COUNT(*) FROM crispframe_gallery_items WHERE foreign_table_parent_uid = ? AND deleted = 0', [$block]);
$content->update('tt_content', ['crispframe_gallery_items' => $count], ['uid' => $block]);
echo "Gallery demo ready.\n";
