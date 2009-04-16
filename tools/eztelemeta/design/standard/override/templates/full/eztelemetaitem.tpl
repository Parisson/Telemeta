{* Telemeta Item - Full view *}

<div class="content-view-full">
    <div class="class-telemetaitem">

    <h2>{$node.data_map.item.content.title|wash}</h2>

    <div class="content-media">
        {include uri="design:content/datatype/view/eztelemetaitem.tpl" 
                 attribute=$node.data_map.item}
    </div>

    </div>
</div>
