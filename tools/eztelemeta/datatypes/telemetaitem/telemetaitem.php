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
class telemetaItem
{
    private $cacheTimeout = 3600;

    private $properties = array(
        'id'            => null,
        'title'         => null,
        'description'   => null,
        'rights'        => null,
        'duration'      => null,
        'creator'       => null,
        'timeFetched'   => null
    );


    /**
     * Constructs a new Telemeta item data type
     *
     * @param   string $data Serialized data
     * @throws  telemetaDatatypeInvalidParamsError
     */
    public function __construct($data = null)
    {
        if ($data) {
            $data = unserialize($data);
            if (!$data) {
                throw new telemetaInvalidParamsError("Couldn't unserialize Telemeta Item data");
            }
            $this->properties = array_merge($this->properties, $data);
        }
    }

    private function fetch($itemId)
    {
        if ($itemId == 1000) {
            $this->properties['id']             = 1000;
            $this->properties['title']          = "Pulp Fiction";
            $this->properties['description']    = "A crazy movie";
            $this->properties['rights']         = "Copyright Holywood";
            $this->properties['duration']       = 3600 + 1800;
            $this->properties['creator']        = "Quentin Tarantino";
            $this->properties['timeFetched']    = time();
            return true;
        }
        return false;
    }

    public function __toString()
    {
        return serialize($this->properties);
    }

    public static function createFromString($str)
    {
        return new self($str);
    }

    public function attribute($name)
    {
        return $this->__get($name);
    }

    public function hasAttribute($name)
    {
        return $this->__isset($name);
    }

    public function __get($name)
    {
        if ($this->__isset($name)) {
            return $this->properties[$name];
        } else {
            throw new ezcBasePropertyNotFoundException($name);
        }
    }

    public function __isset($name)
    {
        return (array_key_exists($name, $this->properties) and !is_null($this->properties[$name]));
    }

    public function hasContent()
    {
        return $this->__isset('id');
    }
}


?>

