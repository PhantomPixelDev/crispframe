<?php

declare(strict_types=1);

/*
 * Local development overrides.
 * TYPO3 loads this file automatically (config/system/additional.php).
 */

if (!str_starts_with((string)getenv('TYPO3_CONTEXT'), 'Development')) {
    return;
}

$trustedHostsPattern = getenv('CRISPFRAME_TRUSTED_HOST_PATTERN');
$GLOBALS['TYPO3_CONF_VARS']['SYS']['trustedHostsPattern'] = $trustedHostsPattern ?: '.*';
$GLOBALS['TYPO3_CONF_VARS']['SYS']['devIPmask'] = '*';
$GLOBALS['TYPO3_CONF_VARS']['BE']['debug'] = true;

$reverseProxyIp = getenv('CRISPFRAME_REVERSE_PROXY_IP');
if ($reverseProxyIp) {
    $GLOBALS['TYPO3_CONF_VARS']['SYS']['reverseProxyHeaderMultiValue'] = 'first';
    $GLOBALS['TYPO3_CONF_VARS']['SYS']['reverseProxyIP'] = $reverseProxyIp;
    $GLOBALS['TYPO3_CONF_VARS']['SYS']['reverseProxySSL'] = $reverseProxyIp;
}

// The local Compose stack captures form mail in Mailpit. Production installs
// configure their own transport and do not set this environment variable.
$devSmtpServer = getenv('CRISPFRAME_DEV_SMTP_SERVER');
if ($devSmtpServer) {
    $GLOBALS['TYPO3_CONF_VARS']['MAIL']['transport'] = 'smtp';
    $GLOBALS['TYPO3_CONF_VARS']['MAIL']['transport_smtp_server'] = $devSmtpServer;
}
