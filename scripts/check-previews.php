<?php
declare(strict_types=1);

// Render the actual Content Blocks preview layouts with representative content.
$root = getenv('CRISPFRAME_PREVIEW_ROOT') ?: dirname(__DIR__);
$loader = require $root . '/vendor/autoload.php';
\TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::run(0, \TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::REQUESTTYPE_CLI);
\TYPO3\CMS\Core\Core\Bootstrap::init($loader);
$factory = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\TYPO3\CMS\Core\View\ViewFactoryInterface::class);
$request = new \TYPO3\CMS\Core\Http\ServerRequest('https://example.invalid/typo3/');
$count = 0;
$theme = getenv('CRISPFRAME_PREVIEW_THEME') ?: (is_dir($root . '/packages/agency_theme') ? $root . '/packages/agency_theme' : $root . '/vendor/crispframe/agency-theme');
foreach (glob($theme . '/ContentBlocks/ContentElements/*/templates/backend-preview.html') as $template) {
    $data = array_fill_keys(['headline', 'name', 'quote', 'lead', 'subheadline', 'bio', 'text', 'body', 'header'], 'Preview <script>unsafe()</script> & content');
    $item = array_fill_keys(['title', 'name', 'label', 'question', 'headline', 'quote', 'caption'], 'Visible preview item');
    $item['systemProperties'] = ['disabled' => false];
    $hidden = array_fill_keys(['title', 'name', 'label', 'question', 'headline', 'quote', 'caption'], 'HIDDEN_PREVIEW_ITEM');
    $hidden['systemProperties'] = ['disabled' => true];
    foreach (['items', 'tiers', 'rows'] as $key) {
        $data[$key] = [$item, $hidden];
    }
    foreach (['Header', 'Content'] as $section) {
        $view = $factory->create(new \TYPO3\CMS\Core\View\ViewFactoryData(
            templateRootPaths: [dirname($template)],
            layoutRootPaths: ['EXT:content_blocks/Resources/Private/Layouts/Preview/' . $section],
            request: $request,
        ));
        $view->assign('data', $data);
        $output = $view->render('backend-preview');
        if (str_contains($output, '<script>') || str_contains($output, 'HIDDEN_PREVIEW_ITEM') || str_contains($output, '<f:')) {
            throw new RuntimeException('Unsafe or unrendered preview: ' . $template . '/' . $section);
        }
    }
    $count++;
}
if ($count !== 27) {
    throw new RuntimeException('Expected 27 block previews, found ' . $count);
}
echo "Rendered $count backend previews safely.\n";
