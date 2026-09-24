<?php

declare(strict_types=1);

namespace Crispframe\AgencyTheme\DataProcessing;

use TYPO3\CMS\Core\Resource\FileRepository;
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
        foreach ($processedData['childPages'] as &$page) {
            $data = $page['data'] ?? [];
            $uid = (int)($data['_LOCALIZED_UID'] ?? $data['uid'] ?? 0);
            $baseUid = (int)($data['uid'] ?? 0);
            $page['teaserSummary'] = trim((string)(($data['abstract'] ?? '') ?: ($data['description'] ?? '')));
            $page['teaserImage'] = null;
            if ($uid <= 0) {
                continue;
            }
            $images = $repository->findByRelation('pages', 'media', $uid);
            if ($images === [] && $baseUid > 0 && $baseUid !== $uid) {
                $images = $repository->findByRelation('pages', 'media', $baseUid);
            }
            $page['teaserImage'] = $images[0] ?? null;
        }
        unset($page);
        return $processedData;
    }
}
