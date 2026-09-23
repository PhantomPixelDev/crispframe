<?php

$EM_CONF[$_EXTKEY] = [
    'title' => 'Crispframe Agency Theme',
    'description' => 'Reusable corporate site package for TYPO3 13.4 LTS with Site Set, content blocks, form and style settings.',
    'category' => 'templates',
    'version' => '1.0.0',
    'state' => 'stable',
    'author' => 'Crispframe',
    'author_email' => '',
    'author_company' => 'Crispframe',
    'constraints' => [
        'depends' => [
            'typo3' => '13.4.0-13.4.99',
            'fluid_styled_content' => '13.4.0-13.4.99',
            'rte_ckeditor' => '13.4.0-13.4.99',
            'content_blocks' => '1.6.0-1.99.99',
            'form' => '13.4.0-13.4.99',
            'frontend' => '13.4.0-13.4.99',
            'seo' => '13.4.0-13.4.99',
        ],
        'conflicts' => [],
        'suggests' => [],
    ],
    'autoload' => [
        'psr-4' => [
            'Crispframe\\AgencyTheme\\' => 'Classes',
        ],
    ],
];
