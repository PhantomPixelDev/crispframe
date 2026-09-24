<?php

declare(strict_types=1);

namespace Crispframe\AgencyTheme\DataProcessing;

use TYPO3\CMS\Core\Context\Context;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Resource\FileRepository;
use TYPO3\CMS\Core\Resource\ResourceFactory;
use TYPO3\CMS\Core\Utility\GeneralUtility;
use TYPO3\CMS\Frontend\ContentObject\ContentObjectRenderer;
use TYPO3\CMS\Frontend\ContentObject\DataProcessorInterface;

final class ChildPageMediaProcessor implements DataProcessorInterface
{
    public function process(
        ContentObjectRenderer $cObj,
        array $contentObjectConfiguration,
        array $processorConfiguration,
        array $processedData,
    ): array {
        if (!isset($processedData['childPages']) || !is_array($processedData['childPages'])) {
            return $processedData;
        }
        $repository = GeneralUtility::makeInstance(FileRepository::class);
        $resources = GeneralUtility::makeInstance(ResourceFactory::class);
        $connections = GeneralUtility::makeInstance(ConnectionPool::class);
        $languageId = (int)GeneralUtility::makeInstance(Context::class)->getPropertyFromAspect('language', 'id');
        foreach ($processedData['childPages'] as &$page) {
            $data = $page['data'] ?? [];
            $uid = (int)($data['_LOCALIZED_UID'] ?? $data['uid'] ?? 0);
            $baseUid = (int)($data['uid'] ?? 0);
            $page['teaserSummary'] = trim((string)(($data['abstract'] ?? '') ?: ($data['description'] ?? '')));
            $page['teaserImage'] = null;
            $page['teaserAlt'] = '';
            if ($uid <= 0) {
                continue;
            }
            if ($languageId > 0 && $baseUid > 0) {
                $translatedUid = $connections->getConnectionForTable('pages')->select(
                    ['uid'],
                    'pages',
                    ['l10n_parent' => $baseUid, 'sys_language_uid' => $languageId, 'deleted' => 0],
                )->fetchOne();
                if ($translatedUid !== false) {
                    $uid = (int)$translatedUid;
                }
            }
            $hasLocalizedImage = false;
            $references = $connections->getConnectionForTable('sys_file_reference');
            if ($languageId > 0 && $baseUid > 0) {
                $baseReferenceUid = $references->select(
                    ['uid'],
                    'sys_file_reference',
                    [
                        'tablenames' => 'pages',
                        'fieldname' => 'media',
                        'uid_foreign' => $baseUid,
                        'sys_language_uid' => 0,
                        'deleted' => 0,
                    ],
                    [],
                    ['sorting_foreign' => 'ASC'],
                    1,
                )->fetchOne();
                if ($baseReferenceUid !== false) {
                    $localizedReferenceUid = $references->select(
                        ['uid'],
                        'sys_file_reference',
                        ['l10n_parent' => (int)$baseReferenceUid, 'sys_language_uid' => $languageId, 'deleted' => 0],
                        [],
                        [],
                        1,
                    )->fetchOne();
                    if ($localizedReferenceUid !== false) {
                        $page['teaserImage'] = $resources->getFileReferenceObject((int)$localizedReferenceUid);
                        $hasLocalizedImage = true;
                    }
                }
            }
            if ($page['teaserImage'] === null) {
                $images = $repository->findByRelation('pages', 'media', $uid);
                if ($images !== []) {
                    $page['teaserImage'] = $images[0];
                    $hasLocalizedImage = $languageId > 0 && $uid !== $baseUid;
                } elseif ($baseUid > 0 && $baseUid !== $uid) {
                    $images = $repository->findByRelation('pages', 'media', $baseUid);
                    $page['teaserImage'] = $images[0] ?? null;
                }
            }
            if ($page['teaserImage'] !== null) {
                $imageAlt = $hasLocalizedImage || $languageId === 0
                    ? $page['teaserImage']->getAlternative() : '';
                $page['teaserAlt'] = trim((string)($imageAlt ?: ($page['title'] ?? '')));
            }
        }
        unset($page);
        return $processedData;
    }
}
