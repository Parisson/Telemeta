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
        $idvar   = "{$base}_itemid_" . $attribute->attribute('id');
        $urlvar  = "{$base}_url_" . $attribute->attribute('id');
        if ($http->hasPostVariable($idvar)) {
            $itemId = trim($http->postVariable($idvar));
            $url    = trim($http->postVariable($urlvar));
            $classAttribute = $attribute->contentClassAttribute();
            if ($classAttribute->attribute("is_required")) {
                if (!$itemId) {
                    $attribute->setValidationError(ezi18n('content/datatypes',
                                                          "A valid Telemeta Item identifier is required",
                                                          __CLASS__));
                    return eZInputValidator::STATE_INVALID;
                }
                if (!$url) {
                    $attribute->setValidationError(ezi18n('content/datatypes',
                                                          "A valid Telemeta URL is required",
                                                          __CLASS__));
                    return eZInputValidator::STATE_INVALID;
                }
            }
            $item = $this->initItem($url, $itemId);
            try {
                $this->fetchItem($item);
            } catch (eZTelemetaError $e) {
                $attribute->setValidationError(ezi18n('content/datatypes', $e->getMessage(), __CLASS__));
                return eZInputValidator::STATE_INVALID;
            }
        }
        return eZInputValidator::STATE_ACCEPTED;
    }

    function initItem($url, $itemId)
    {
        return array(
            'id'            => $itemId,
            'url'           => $url,
            'title'         => '',
            'creator'       => '',
            'description'   => '',
            'rights'        => ''
        );
    }

    function fetchItem($item)
    {
        $url  = $item['url'];
        if (!ereg('^http://', $url)) {
            $url = "http://$url";
        }
        $url = ereg_replace('/*$', '', $url);
        $id = urlencode('item:' . $item['id']);
        $request    = "$url/oai/?verb=GetRecord&identifier=$id&metadataPrefix=oai_dc";

        $doc = new DOMDocument();
        if (!@$doc->load($request)) {
            throw new eZTelemetaError("The Telemeta server couldn't be reached or returned malformed XML (request: $request)");
        }

        $root = $doc->getElementsByTagName('OAI-PMH');
        if (!$root->length)
            throw new eZTelemetaError("Retrieved XML document isn't a valid OAI-PMH response");

        $root = $root->item(0);
        $error = $root->getElementsByTagName('error');
        if ($error->length) {
            $msg = $error->item(0)->firstChild->nodeValue;
            throw new eZTelemetaError("Telemeta OAI-PMH error: $msg");
        }

        $record = $root->getElementsByTagName('GetRecord');
        if (!$record->length) {
            throw new eZTelemetaError("Retrieved XML document isn't a valid OAI-PMH response (missing GetRecord tag)");
        }

        $dc = $record->item(0)->getElementsByTagNameNS('*', 'dc')->item(0);
        $result = $this->initItem($item['url'], $item['id']);
        foreach ($dc->childNodes as $element) {
            if ($element->nodeType == XML_ELEMENT_NODE) {
                $tag = str_replace('dc:', '', $element->tagName);
                if (array_key_exists($tag, $result) and empty($result[$tag])) {
                    $result[$tag] = trim($element->firstChild->nodeValue);
                }
            }
        }

        if (!$result['title']) {
            throw new eZTelemetaError("The retrieved item has no title");
        }

        return array_merge($item, $result);
    }

    function fetchObjectAttributeHTTPInput($http, $base, $attribute)
    {
        $idvar  = "{$base}_itemid_" . $attribute->attribute('id');
        $urlvar = "{$base}_url_" . $attribute->attribute('id');
        if ($http->hasPostVariable($idvar)) {
            $itemId = trim($http->postVariable($idvar));
            $url    = trim($http->postVariable($urlvar));
            $item   = $this->initItem($url, $itemId);
            try {
                $item = $this->fetchItem($item);
            } catch (eZTelemetaError $e) {
            }
            $attribute->setAttribute("data_text", serialize($item));
        }
        return true;
    }

    function objectAttributeContent($attribute)
    {
        $item = unserialize($attribute->attribute("data_text"));
        try {
            $filled = $this->fetchItem($item);
            return $filled;
        } catch (eZTelemetaError $e) {
            return $item;
        }
    }

    function metaData($attribute)
    {
        $data = unserialize($attribute->attribute("data_text"));
        $words = array();
        $src = $data['title'] . ' ' . $data['description'];
        $cut = split('[ =+()[{}_,.:;\\/"\'*#%!?&-]+', $src);
        foreach ($cut as $w) {
            if (strlen($w) >= 3) {
                $words[] = $w;
            }
        }
        $words = join(" ", $words);
        file_put_contents("/tmp/c{$data['id']}", $words);
        return $words;
    }

    function title($attribute, $name = null)
    {
        $data = unserialize($attribute->attribute("data_text"));
        if (!$data['title'])
            return 'untitled';
        return $data['title'];
    }

    function isIndexable()
    {
        return true;
    }

}

class eZTelemetaError extends ezcBaseException
{
    public function __construct($msg)
    {
        parent::__construct($msg);
    }

}

eZDataType::register(eZTelemetaItemType::DATA_TYPE_STRING, "eztelemetaitemtype");
