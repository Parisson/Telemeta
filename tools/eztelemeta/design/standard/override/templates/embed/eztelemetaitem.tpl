{eztelemetadata_set('eztelemeta_player', true)}
<div class="view-embed">
    <div class="content-media">
    {let attribute=$object.data_map.item}
        Telemeta Item:
        <dl>
        <dt>Server:</dt><dd>{$attribute.content.url}</dd>
        <dt>Identifier:</dt><dd>{$attribute.content.id}</dd>
        <dt>Title:</dt><dd>{$attribute.content.title|wash}</dd>
        </dl>
        <ul class="ezt-playlist">
        <li>
            <a class="ezt-playable" href="{$attribute.content.mp3}">{$attribute.content.title|wash}</a>
            <div class="ezt-metadata">
                <div class="ezt-duration">{$attribute.content.duration_str}</div>
                <ul></ul>
            </div>
         </li>
        </ul>
    {/let}
    </div>
</div>

