<?php

declare(strict_types=1);

defined('TYPO3') or die();

// The Form backend module has no page context, so it needs the configuration
// path globally. Frontend TypoScript is supplied by the Site Set.
\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addTypoScriptSetup(
    'module.tx_form.settings.yamlConfigurations.100 = EXT:agency_theme/Configuration/Form/FormSetup.yaml'
);
