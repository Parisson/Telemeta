<?php
/*
 * eZTelemeta page data handling
 *
 * Copyright (c) 2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: CeCILL Free Software License Agreement
 */

$eZTemplateOperatorArray = array();
$eZTemplateOperatorArray[] = array( 'script' => 'extension/eztelemeta/autoloads/eztelemetadata.php',
                                    'class' => 'eZTelemetaData',
                                    'operator_names' => array( 'eztelemetadata_set', 'eztelemetadata_append' ) );
?>
