<?php
declare(strict_types=1);

// Repeatable local demo content. Run inside the PHP container:
// php /app/config/seed-demo.php
$loader = require dirname(__DIR__) . '/vendor/autoload.php';
\TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::run(0, \TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::REQUESTTYPE_CLI);
\TYPO3\CMS\Core\Core\Bootstrap::init($loader);

$pool = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\TYPO3\CMS\Core\Database\ConnectionPool::class);
$pages = $pool->getConnectionForTable('pages');
$content = $pool->getConnectionForTable('tt_content');
$root = $pages->fetchAssociative('SELECT uid FROM pages WHERE uid = 1 AND deleted = 0');
if (!$root) {
    throw new RuntimeException('Create the root page (uid 1) before seeding the demo.');
}

$now = time();
$ensurePage = static function (string $title, string $slug, int $sorting, bool $inMenu = true) use ($pages, $now): int {
    $existing = $pages->fetchOne('SELECT uid FROM pages WHERE pid = 1 AND slug = ? AND deleted = 0', [$slug]);
    if ($existing) {
        return (int)$existing;
    }
    $pages->insert('pages', [
        'pid' => 1, 'title' => $title, 'slug' => $slug, 'doktype' => 1,
        'sorting' => $sorting, 'hidden' => 0, 'nav_hide' => $inMenu ? 0 : 1,
        'crdate' => $now, 'tstamp' => $now,
    ]);
    return (int)$pages->lastInsertId();
};

$ensureBlock = static function (int $page, int $sorting, string $type, string $marker, array $fields) use ($content, $now): int {
    $existing = $content->fetchOne('SELECT uid FROM tt_content WHERE pid = ? AND header = ? AND deleted = 0', [$page, $marker]);
    if ($existing) {
        return (int)$existing;
    }
    $content->insert('tt_content', array_merge([
        'pid' => $page, 'CType' => $type, 'header' => $marker,
        'colPos' => 0, 'sorting' => $sorting, 'hidden' => 0,
        'crdate' => $now, 'tstamp' => $now,
    ], $fields));
    return (int)$content->lastInsertId();
};

$ensureItems = static function (string $table, int $parent, int $page, array $items, string $key = 'title') use ($pool, $content, $now): void {
    $connection = $pool->getConnectionForTable($table);
    foreach ($items as $index => $item) {
        $existing = $connection->fetchOne(
            "SELECT uid FROM {$table} WHERE foreign_table_parent_uid = ? AND {$key} = ? AND deleted = 0",
            [$parent, $item[$key]]
        );
        if ($existing) {
            if (isset($item['icon'])) {
                $savedIcon = $connection->fetchOne("SELECT icon FROM {$table} WHERE uid = ?", [$existing]);
                if ($savedIcon === '' || $savedIcon === 'none') {
                    $connection->update($table, ['icon' => $item['icon'], 'tstamp' => $now], ['uid' => $existing]);
                }
            }
            if (!empty($item['hideSuffix'])) {
                $connection->update($table, ['hideSuffix' => 1, 'tstamp' => $now], ['uid' => $existing]);
            }
            continue;
        }
        $connection->insert($table, array_merge([
            'pid' => $page, 'foreign_table_parent_uid' => $parent,
            'sorting' => ($index + 1) * 128, 'hidden' => 0,
            'crdate' => $now, 'tstamp' => $now,
        ], $item));
    }
    $count = (int)$connection->fetchOne(
        "SELECT COUNT(uid) FROM {$table} WHERE foreign_table_parent_uid = ? AND deleted = 0",
        [$parent]
    );
    $content->update('tt_content', [$table => $count, 'tstamp' => $now], ['uid' => $parent]);
};

$work = $ensurePage('Work', '/work', 128);
$contact = $ensurePage('Contact', '/contact', 256);
$components = $ensurePage('Components', '/components', 384, false);

$ensureBlock(1, 128, 'crispframe_hero', 'Demo: home hero', [
    'crispframe_hero_eyebrow' => 'Strategy · Design · Engineering',
    'crispframe_hero_headline' => 'Digital experiences built with clarity',
    'crispframe_hero_subheadline' => 'We turn complex ideas into accessible websites and digital products that are a pleasure to use.',
    'crispframe_hero_primaryLinkLabel' => 'Start a project',
    'crispframe_hero_primaryLink' => '/contact',
    'crispframe_hero_secondaryLinkLabel' => 'Explore our work',
    'crispframe_hero_secondaryLink' => '/work',
    'crispframe_hero_isHero' => 1,
    'crispframe_hero_sectionSpacing' => 'large',
    'crispframe_hero_sectionBackground' => 'subtle',
    'crispframe_hero_width' => 'wide',
]);
$ensureBlock(1, 256, 'crispframe_intro', 'Demo: approach', [
    'crispframe_intro_headline' => 'Good work starts with understanding',
    'crispframe_intro_lead' => 'A focused team for the whole journey.',
    'crispframe_intro_text' => 'We connect research, design and implementation so every decision serves your customers and your business.',
    'crispframe_intro_linkLabel' => 'See what we do',
    'crispframe_intro_link' => '/work',
    'crispframe_intro_sectionSpacing' => 'large',
    'crispframe_intro_sectionBackground' => 'default',
    'crispframe_intro_width' => 'narrow',
]);
$services = $ensureBlock(1, 320, 'crispframe_services', 'Demo: services', [
    'crispframe_services_headline' => 'What we can build together',
    'crispframe_services_lead' => 'A flexible starting point for your own service offering.',
    'crispframe_services_sectionSpacing' => 'default',
    'crispframe_services_sectionBackground' => 'subtle',
    'crispframe_services_width' => 'default',
]);
$ensureItems('crispframe_services_items', $services, 1, [
    ['title' => 'Strategy', 'description' => 'Turn business goals and user needs into a focused digital plan.', 'icon' => 'compass', 'link' => '/contact', 'linkLabel' => 'Discuss a project'],
    ['title' => 'Design', 'description' => 'Create clear interfaces and a visual language that fits your organisation.', 'icon' => 'layers-3', 'link' => '/contact', 'linkLabel' => 'Discuss a project'],
    ['title' => 'Engineering', 'description' => 'Build maintainable TYPO3 websites and digital experiences.', 'icon' => 'workflow', 'link' => '/contact', 'linkLabel' => 'Discuss a project'],
]);
$features = $ensureBlock(1, 352, 'crispframe_featuregrid', 'Demo: features', [
    'crispframe_featuregrid_headline' => 'Made for the people behind the website',
    'crispframe_featuregrid_lead' => 'A good platform should work for visitors and editors alike.',
    'crispframe_featuregrid_sectionSpacing' => 'default',
    'crispframe_featuregrid_sectionBackground' => 'default',
    'crispframe_featuregrid_width' => 'default',
]);
$ensureItems('crispframe_featuregrid_items', $features, 1, [
    ['title' => 'Accessible by design', 'description' => 'Readable content, clear navigation and keyboard-friendly interactions.', 'icon' => 'shield-check'],
    ['title' => 'Easy to edit', 'description' => 'Structured blocks let teams update pages without rebuilding layouts.', 'icon' => 'puzzle'],
    ['title' => 'Ready to evolve', 'description' => 'Reusable page patterns provide room for new content and services.', 'icon' => 'rocket'],
]);
$ensureBlock(1, 384, 'crispframe_cta', 'Demo: home CTA', [
    'crispframe_cta_headline' => 'Have a challenge worth solving?',
    'crispframe_cta_text' => 'Tell us what you are working on. We will help you find a practical next step.',
    'crispframe_cta_primaryLinkLabel' => 'Get in touch',
    'crispframe_cta_primaryLink' => '/contact',
    'crispframe_cta_sectionSpacing' => 'large',
    'crispframe_cta_sectionBackground' => 'brand',
    'crispframe_cta_width' => 'default',
]);
$ensureBlock($work, 64, 'crispframe_hero', 'Demo: work hero', [
    'crispframe_hero_eyebrow' => 'Selected work',
    'crispframe_hero_headline' => 'Work with purpose',
    'crispframe_hero_subheadline' => 'Clear thinking and careful execution for digital experiences that last.',
    'crispframe_hero_isHero' => 1,
    'crispframe_hero_sectionSpacing' => 'large',
    'crispframe_hero_sectionBackground' => 'subtle',
    'crispframe_hero_width' => 'wide',
]);
$ensureBlock($work, 128, 'crispframe_intro', 'Demo: work intro', [
    'crispframe_intro_headline' => 'Work shaped around real needs',
    'crispframe_intro_lead' => 'From first question to a dependable launch.',
    'crispframe_intro_text' => 'Our projects bring content, interaction and technology into one coherent experience. Add your case studies here using the Projects content block.',
    'crispframe_intro_sectionSpacing' => 'large',
    'crispframe_intro_sectionBackground' => 'subtle',
    'crispframe_intro_width' => 'narrow',
]);
$projects = $ensureBlock($work, 256, 'crispframe_projects', 'Demo: project examples', [
    'crispframe_projects_headline' => 'Example project formats',
    'crispframe_projects_lead' => 'Replace these illustrative entries with your own case studies.',
    'crispframe_projects_sectionSpacing' => 'default',
    'crispframe_projects_sectionBackground' => 'default',
    'crispframe_projects_width' => 'default',
]);
$ensureItems('crispframe_projects_items', $projects, $work, [
    ['title' => 'Corporate website', 'category' => 'Example', 'description' => 'A clear presentation of services, people and expertise.'],
    ['title' => 'Customer portal', 'category' => 'Example', 'description' => 'A focused workspace for recurring customer tasks.'],
    ['title' => 'Editorial platform', 'category' => 'Example', 'description' => 'A flexible publishing experience for distributed teams.'],
]);
$ensureBlock($contact, 64, 'crispframe_hero', 'Demo: contact hero', [
    'crispframe_hero_eyebrow' => 'Contact',
    'crispframe_hero_headline' => 'Start a conversation',
    'crispframe_hero_subheadline' => 'We would love to hear what you are building.',
    'crispframe_hero_isHero' => 1,
    'crispframe_hero_sectionSpacing' => 'large',
    'crispframe_hero_sectionBackground' => 'subtle',
    'crispframe_hero_width' => 'wide',
]);
$ensureBlock($contact, 128, 'crispframe_contact', 'Demo: contact details', [
    'crispframe_contact_headline' => 'Let us talk',
    'crispframe_contact_lead' => 'Share your idea, brief or question.',
    'crispframe_contact_email' => 'hello@crispframe.example',
    'crispframe_contact_phone' => '+49 30 000000',
    'crispframe_contact_address' => 'Torstraße 140, 10119 Berlin',
    'crispframe_contact_note' => 'Demo contact details: replace these values in the content element and site settings before launch.',
    'crispframe_contact_sectionSpacing' => 'large',
    'crispframe_contact_sectionBackground' => 'default',
    'crispframe_contact_width' => 'default',
]);
$formPath = 'EXT:agency_theme/Resources/Private/Forms/Contact.form.yaml';
$formFlexform = '<?xml version="1.0" encoding="utf-8"?>'
    . '<T3FlexForms><data><sheet index="sDEF"><language index="lDEF">'
    . '<field index="settings.persistenceIdentifier"><value index="vDEF">'
    . htmlspecialchars($formPath, ENT_XML1)
    . '</value></field></language></sheet></data></T3FlexForms>';
$ensureBlock($contact, 256, 'form_formframework', 'Demo: contact form', [
    'pi_flexform' => $formFlexform,
]);

$pricing = $ensureBlock($components, 128, 'crispframe_pricing', 'Demo: pricing', [
    'crispframe_pricing_headline' => 'Flexible ways to work together',
    'crispframe_pricing_lead' => 'Illustrative service tiers. Replace these prices and benefits with your own offer.',
    'crispframe_pricing_monthlySuffix' => '/ month',
    'crispframe_pricing_yearlySuffix' => '/ month, billed yearly',
    'crispframe_pricing_footnote' => 'Example prices only; scope and taxes depend on your agreement.',
    'crispframe_pricing_sectionBackground' => 'subtle',
    'crispframe_pricing_sectionSpacing' => 'default',
    'crispframe_pricing_width' => 'default',
]);
$ensureItems('crispframe_pricing_tiers', $pricing, $components, [
    ['name' => 'Essentials', 'summary' => 'A strong start for focused teams.', 'monthlyPrice' => '€950', 'yearlyPrice' => '€790', 'features' => '<ul><li>Content and design review</li><li>Monthly improvement plan</li><li>Email support</li></ul>', 'ctaLabel' => 'Ask about Essentials', 'ctaLink' => '/contact', 'featured' => 0],
    ['name' => 'Growth', 'summary' => 'Ongoing design and development.', 'monthlyPrice' => '€2,400', 'yearlyPrice' => '€2,050', 'features' => '<ul><li>Continuous TYPO3 improvements</li><li>Priority support</li><li>Monthly strategy session</li></ul>', 'ctaLabel' => 'Talk about Growth', 'ctaLink' => '/contact', 'featured' => 1],
    ['name' => 'Partner', 'summary' => 'A dedicated team for complex work.', 'monthlyPrice' => 'On request', 'yearlyPrice' => 'On request', 'hideSuffix' => 1, 'features' => '<ul><li>Dedicated delivery team</li><li>Product planning</li><li>Custom service agreement</li></ul>', 'ctaLabel' => 'Plan a partnership', 'ctaLink' => '/contact', 'featured' => 0],
], 'name');
$ensureBlock($components, 256, 'crispframe_video', 'Demo: privacy-friendly video', [
    'crispframe_video_headline' => 'A video that waits for your click',
    'crispframe_video_lead' => 'The video provider is not contacted until you press play.',
    'crispframe_video_provider' => 'youtube',
    'crispframe_video_videoId' => 'M7lc1UVf-VE',
    'crispframe_video_caption' => 'Example embed. Replace the video ID, poster and transcript with your own content.',
    'crispframe_video_transcript' => 'This is an example video block. Add a full transcript when publishing your own video.',
    'crispframe_video_sectionBackground' => 'default',
    'crispframe_video_sectionSpacing' => 'default',
    'crispframe_video_width' => 'default',
]);

// Keep a specimen of every block on the hidden Components page. These records
// are regular editable content, and are included in the optional demo export.
$ensureBlock($components, 512, 'crispframe_textimage', 'Demo: text and image', [
    'crispframe_textimage_headline' => 'Content with room to breathe',
    'crispframe_textimage_lead' => 'A flexible editorial layout.',
    'crispframe_textimage_text' => 'Pair a short story with an image, or leave the image empty when the words stand on their own.',
    'crispframe_textimage_imagePosition' => 'right',
    'crispframe_textimage_sectionBackground' => 'subtle',
    'crispframe_textimage_sectionSpacing' => 'default',
    'crispframe_textimage_width' => 'default',
]);
$stats = $ensureBlock($components, 640, 'crispframe_stats', 'Demo: statistics', [
    'crispframe_stats_headline' => 'Numbers with a clear meaning',
    'crispframe_stats_lead' => 'Replace illustrative values with verified results.',
    'crispframe_stats_sectionBackground' => 'dark',
    'crispframe_stats_sectionSpacing' => 'default',
    'crispframe_stats_width' => 'default',
]);
$ensureItems('crispframe_stats_items', $stats, $components, [
    ['value' => '24', 'label' => 'example launches'],
    ['value' => '8', 'label' => 'years of collaboration'],
    ['value' => '4', 'label' => 'specialist disciplines'],
], 'value');
$logos = $ensureBlock($components, 768, 'crispframe_logocloud', 'Demo: logo cloud', [
    'crispframe_logocloud_headline' => 'Partners and collaborators',
    'crispframe_logocloud_lead' => 'Use logos only when you have permission.',
    'crispframe_logocloud_sectionBackground' => 'brand',
    'crispframe_logocloud_sectionSpacing' => 'default',
    'crispframe_logocloud_width' => 'default',
]);
$ensureItems('crispframe_logocloud_items', $logos, $components, [
    ['name' => 'Example partner one'],
    ['name' => 'Example partner two'],
    ['name' => 'Example partner three'],
], 'name');
$quotes = $ensureBlock($components, 896, 'crispframe_testimonials', 'Demo: testimonials', [
    'crispframe_testimonials_headline' => 'What collaboration can feel like',
    'crispframe_testimonials_lead' => 'Replace these fictional quotes with approved testimonials.',
    'crispframe_testimonials_sectionBackground' => 'subtle',
    'crispframe_testimonials_sectionSpacing' => 'default',
    'crispframe_testimonials_width' => 'default',
]);
$ensureItems('crispframe_testimonials_items', $quotes, $components, [
    ['quote' => 'The team made a complex brief feel manageable.', 'author' => 'Example person', 'role' => 'Example organization'],
], 'author');
$team = $ensureBlock($components, 1024, 'crispframe_team', 'Demo: team', [
    'crispframe_team_headline' => 'The people behind the work',
    'crispframe_team_lead' => 'Introduce real people with their consent.',
    'crispframe_team_sectionBackground' => 'brand',
    'crispframe_team_sectionSpacing' => 'default',
    'crispframe_team_width' => 'default',
]);
$ensureItems('crispframe_team_items', $team, $components, [
    ['name' => 'Alex Example', 'role' => 'Design lead', 'bio' => 'Shapes clear interfaces and content systems.'],
    ['name' => 'Sam Example', 'role' => 'Technical lead', 'bio' => 'Builds maintainable publishing experiences.'],
], 'name');
$process = $ensureBlock($components, 1152, 'crispframe_process', 'Demo: process', [
    'crispframe_process_headline' => 'A practical path from idea to launch',
    'crispframe_process_lead' => 'Give visitors a simple view of what happens next.',
    'crispframe_process_sectionBackground' => 'dark',
    'crispframe_process_sectionSpacing' => 'default',
    'crispframe_process_width' => 'default',
]);
$ensureItems('crispframe_process_items', $process, $components, [
    ['title' => 'Discover', 'description' => 'Agree on goals, audiences and constraints.'],
    ['title' => 'Create', 'description' => 'Design and build the right solution.'],
    ['title' => 'Improve', 'description' => 'Learn from use and refine the experience.'],
], 'title');
$faq = $ensureBlock($components, 1280, 'crispframe_faq', 'Demo: frequently asked questions', [
    'crispframe_faq_headline' => 'Questions worth answering',
    'crispframe_faq_lead' => 'Keep answers brief and specific.',
    'crispframe_faq_sectionBackground' => 'default',
    'crispframe_faq_sectionSpacing' => 'default',
    'crispframe_faq_width' => 'default',
]);
$ensureItems('crispframe_faq_items', $faq, $components, [
    ['question' => 'Can I update the content myself?', 'answer' => 'Yes. Each section is an editable TYPO3 content element.'],
    ['question' => 'Can I use a different color palette?', 'answer' => 'Yes. Choose a palette in the site settings.'],
], 'question');

echo "Demo pages and content are ready.\n";
