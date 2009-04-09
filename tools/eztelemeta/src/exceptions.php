<?php
/**
 * Definition of the Telemeta invalid params error
 *
 * @package     eztelemeta
 * @author      Olivier Guilyardi
 * @copyright   2009 Samalyse
 * @license     CeCILL Free Software License Agreement
 */


/**
 * Class defining the Telemeta invalid params error
 *
 * @package     eztelemeta
 * @author      Olivier Guilyardi
 * @copyright   2009 Samalyse
 * @license     CeCILL Free Software License Agreement
 */
class TelemetaInvalidParamsError extends ezcBaseException
{
    public function __construct($msg)
    {
        parent::__construct($msg);
    }
}
?>
