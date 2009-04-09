<?php
/**
 * Definition of the Telemeta Item datatype
 *
 * @package     eztelemeta
 * @author      Olivier Guilyardi
 * @copyright   2009 Samalyse
 * @license     CeCILL Free Software License Agreement
 */


/**
 * Class definining the Telemeta Item datatype
 *
 * @package     eztelemeta
 * @author      Olivier Guilyardi
 * @copyright   2009 Samalyse
 * @license     CeCILL Free Software License Agreement
 */
class eZTelemetaItemType extends eZDataType
{
    const DATA_TYPE_STRING = 'eztelemetaitem';

    public function __construct() 
    {
        parent::__construct(self::DATA_TYPE_STRING, 'Telemeta Item');
    }
    
    function validateObjectAttributeHTTPInput($http, $base, $attribute)
    {
        $idvar = "{$base}_itemid_{$attribute->id}";
        if ($http->hasPostVariable($idvar)) {
            $itemId = $http->postVariable($idvar);
            $classAttribute = $attribute->contentClassAttribute();
            if ($classAttribute->attribute("is_required")) {
                if (!$itemId) {
                    $attribute->setValidationError(ezi18n('content/datatypes',
                                                          "A valid Telemeta Item identifier is required",
                                                          __CLASS__));
                    return eZInputValidator::STATE_INVALID;
                }
            }
            if ($itemId != 1000) {
                $attribute->setValidationError(ezi18n('content/datatypes',
                                                      "Invalid Telemeta Item identifier",
                                                      __CLASS__));
                return eZInputValidator::STATE_INVALID;
            }
        }
        return eZInputValidator::STATE_ACCEPTED;
    }

    function fetchObjectAttributeHTTPInput($http, $base, $attribute)
    {
        $idvar = "{$base}_itemid_{$attribute->id}";
        if ($http->hasPostVariable($idvar)) {
            $itemId = $http->postVariable($idvar);
            $attribute->setAttribute("itemid", $itemId);
        }
        return true;
    }

    function objectAttributeContent($attribute)
    {
        return $attribute->attribute("itemid");
    }

    function metaData($attribute)
    {
        return $attribute->attribute("itemid");
    }

    function title($attribute, $name = null)
    {
        return "Telemeta Item id " . $attribute->attribute("itemid");
    }

    function isIndexable()
    {
        return true;
    }

}

eZDataType::register(eZTelemetaItemType::DATA_TYPE_STRING, "eztelemetaitemtype");
