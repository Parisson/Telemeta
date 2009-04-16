<?php
/*
 * eZTelemeta page data handling
 *
 * Note: this is a simplified version of the eZPageData utility from ezwebin (GPL)
 *
 * Copyright (c) 1999-2009 eZ Systems AS, 2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: CeCILL Free Software License Agreement
 */

/*
 Template operator to speed up page settings and style init time
 Gets its parameters directly from template.
 module_result.path | content_info | persistant_variable | menu.ini ++
 are all used to generate page data, what menues to show
 and so on.  
 
*/

class eZTelemetaData
{
    function eZTelemetaData()
    {
    }

    function operatorList()
    {
        return array( 'eztelemetadata_set', 'eztelemetadata_append' );
    }

    function namedParameterPerOperator()
    {
        return true;
    }

    function namedParameterList()
    {
        return array( 'eztelemetadata_set' => array( 
                              'key' => array( 'type' => 'string',
                                              'required' => true,
                                              'default' => false ),
                            'value' => array( 'type' => 'mixed',
                                              'required' => true,
                                              'default' => false ) ),
                      'eztelemetadata_append' => array( 
                              'key' => array( 'type' => 'string',
                                              'required' => true,
                                              'default' => false ),
                            'value' => array( 'type' => 'mixed',
                                              'required' => true,
                                              'default' => false ) ) );
    }

    function modify( $tpl, $operatorName, $operatorParameters, $rootNamespace, $currentNamespace, &$operatorValue, $namedParameters )
    {
        switch ( $operatorName )
        {
            // note: these functions are not cache-block safe
            // as in: if called inside a cache-block then they will not be called when cache is used.
            case 'eztelemetadata_set':
            case 'eztelemetadata_append':
            {
                self::setPersistentVariable( $namedParameters['key'], $namedParameters['value'], $tpl, $operatorName === 'eztelemetadata_append' );
            }break;
        }
    }

    // reusable function for setting persistent_variable
    static public function setPersistentVariable( $key, $value, $tpl, $append = false )
    {
        $persistentVariable = array();
        if ( $tpl->hasVariable('persistent_variable') && is_array( $tpl->variable('persistent_variable') ) )
        {
           $persistentVariable = $tpl->variable('persistent_variable');
        }
        else if ( self::$persistentVariable !== null && is_array( self::$persistentVariable ) )
        {
            $persistentVariable = self::$persistentVariable;
        }

        if ( $append )
        {
            if ( isset( $persistentVariable[ $key ] ) && is_array( $persistentVariable[ $key ] ) )
            {
                $persistentVariable[ $key ][] = $value;
            }
            else
            {
                $persistentVariable[ $key ] = array( $value );
            }
        }
        else
        {
            $persistentVariable[ $key ] = $value;
        }

        // set the finnished array in the template
        $tpl->setVariable('persistent_variable', $persistentVariable);
        
        // storing the value internally as well in case this is not a view that supports persistent_variable (eztelemetadata will look for it)
        self::$persistentVariable = $persistentVariable;
    }
    
    // reusable function for getting persistent_variable
    static public function getPersistentVariable( $key = null )
    {
        if ( $key !== null )
        {
            if ( isset( self::$persistentVariable[ $key ] ) )
                return self::$persistentVariable[ $key ];
            return null;
        }
        return self::$persistentVariable;
    }

    // Internal version of the $persistent_variable used on view that don't support it
    static protected $persistentVariable = null;
    
}

?>
