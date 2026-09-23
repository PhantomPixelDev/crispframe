<?php
declare(strict_types=1);
require dirname(__DIR__) . '/vendor/autoload.php';
\TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::run(0, \TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::REQUESTTYPE_CLI);
\TYPO3\CMS\Core\Core\Bootstrap::init(
    require dirname(__DIR__) . '/vendor/autoload.php'
);

$container = \TYPO3\CMS\Core\Utility\GeneralUtility::getContainer();
try {
echo 'Environment paths:' . PHP_EOL;
echo '  projectPath: ' . \TYPO3\CMS\Core\Core\Environment::getProjectPath() . PHP_EOL;
echo '  configPath:  ' . \TYPO3\CMS\Core\Core\Environment::getConfigPath() . PHP_EOL;
echo '  varPath:     ' . \TYPO3\CMS\Core\Core\Environment::getVarPath() . PHP_EOL;
echo '  publicPath:  ' . \TYPO3\CMS\Core\Core\Environment::getPublicPath() . PHP_EOL;
echo '  currentScript: ' . \TYPO3\CMS\Core\Core\Environment::getCurrentScript() . PHP_EOL;

$siteConfig = $container->get(\TYPO3\CMS\Core\Configuration\SiteConfiguration::class);
$paths = $siteConfig->getAllSiteConfigurationPaths();
echo 'config paths searched: ' . PHP_EOL;
foreach ($paths as $id => $p) {
    echo $id . ' -> ' . $p . PHP_EOL;
}
echo 'configPath property: ' . PHP_EOL;
$rp = new ReflectionProperty(\TYPO3\CMS\Core\Configuration\SiteConfiguration::class, 'configPath');
echo $rp->getValue($siteConfig) . PHP_EOL;
} catch (\Throwable $e) {
    echo 'EXCEPTION: ' . get_class($e) . ': ' . $e->getMessage() . PHP_EOL;
    echo $e->getTraceAsString() . PHP_EOL;
};