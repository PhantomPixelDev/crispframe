<?php
declare(strict_types=1);

// Boot TYPO3 to create demo pages through the DataHandler.
// Usage: php create-rootpage.php

call_user_func(function (): void {
    $classLoader = require dirname(__DIR__) . '/vendor/autoload.php';
    \TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::run(0, \TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::REQUESTTYPE_CLI);
    \TYPO3\CMS\Core\Core\Bootstrap::init($classLoader);
    $connection = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\TYPO3\CMS\Core\Database\ConnectionPool::class)
        ->getConnectionForTable('pages');

    $count = (int)$connection->count('uid', 'pages', []);
    if ($count > 0) {
        echo "Root page(s) already exist ({$count}). Skipping.\n";
        return;
    }

    $now = time();
    $connection->insert('pages', [
        'pid' => 0,
        't3ver_oid' => 0,
        't3ver_wsid' => 0,
        't3ver_state' => 0,
        't3ver_stage' => 0,
        'hidden' => 0,
        'deleted' => 0,
        'sorting' => 128,
        'title' => 'Home',
        'doktype' => 1,
        'is_siteroot' => 1,
        'slug' => '/',
        'perms_userid' => 1,
        'perms_groupid' => 0,
        'perms_user' => 31,
        'perms_group' => 31,
        'perms_everybody' => 31,
        'crdate' => $now,
        'tstamp' => $now,
    ]);
    echo "Root page created (uid 1).\n";
});