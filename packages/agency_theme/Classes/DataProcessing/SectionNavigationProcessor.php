<?php

declare(strict_types=1);

namespace Crispframe\AgencyTheme\DataProcessing;

use TYPO3\CMS\Core\Context\Context;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Utility\GeneralUtility;
use TYPO3\CMS\Frontend\ContentObject\ContentObjectRenderer;
use TYPO3\CMS\Frontend\ContentObject\DataProcessorInterface;

final class SectionNavigationProcessor implements DataProcessorInterface
{
    public function process(
        ContentObjectRenderer $cObj,
        array $contentObjectConfiguration,
        array $processorConfiguration,
        array $processedData,
    ): array {
        $data = $processedData['data'] ?? null;
        if (is_object($data) && method_exists($data, 'getPid') && method_exists($data, 'getUid')) {
            $pageId = (int)$data->getPid();
            $currentUid = (int)$data->getUid();
        } else {
            $pageId = (int)($data['pid'] ?? 0);
            $currentUid = (int)($data['uid'] ?? 0);
        }
        if ($pageId <= 0) {
            $processedData['sectionNavigation'] = [];
            return $processedData;
        }

        $languageId = (int)GeneralUtility::makeInstance(Context::class)
            ->getPropertyFromAspect('language', 'id');
        $queryBuilder = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getQueryBuilderForTable('tt_content');
        $rows = $queryBuilder
            ->select('uid', 'header')
            ->from('tt_content')
            ->where(
                $queryBuilder->expr()->eq('pid', $queryBuilder->createNamedParameter($pageId)),
                $queryBuilder->expr()->eq('sys_language_uid', $queryBuilder->createNamedParameter($languageId)),
                $queryBuilder->expr()->eq('sectionIndex', $queryBuilder->createNamedParameter(1)),
                $queryBuilder->expr()->neq('uid', $queryBuilder->createNamedParameter($currentUid)),
                $queryBuilder->expr()->neq('header', $queryBuilder->createNamedParameter('')),
            )
            ->orderBy('colPos', 'ASC')
            ->addOrderBy('sorting', 'ASC')
            ->executeQuery()
            ->fetchAllAssociative();

        $processedData['sectionNavigation'] = array_map(
            static fn(array $row): array => [
                'title' => trim((string)$row['header']),
                'anchor' => 'c' . (int)$row['uid'],
            ],
            $rows,
        );
        return $processedData;
    }
}
