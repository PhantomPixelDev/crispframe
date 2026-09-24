<?php

$EM_CONF[$_EXTKEY] = [
    'title' => 'Crispframe Example Pages',
    'description' => 'Optional example page tree for a fresh Crispframe installation.',
    'category' => 'distribution',
    'version' => '1.4.0',
    'state' => 'stable',
    'author' => 'Crispframe',
    'constraints' => [
        'depends' => [
            'typo3' => '13.4.15-14.3.99',
            'agency_theme' => '1.4.0-1.99.99',
            'impexp' => '13.4.15-14.3.99',
        ],
        'conflicts' => [],
        'suggests' => [],
    ],
];
