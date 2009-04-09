<div class="view-embed">
    <div class="content-media">
    {let attribute=$object.data_map.item}
        Telemeta Item:
        <dl>
        <dt>Server:</dt><dd>{$attribute.content.url}</dd>
        <dt>Identifier:</dt><dd>{$attribute.content.id}</dd>
        <dt>Title:</dt><dd>{$attribute.content.title|wash}</dd>
        </dl>
    {/let}
    </div>
</div>

