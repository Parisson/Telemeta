{eztelemetadata_set('eztelemeta_player', true)}
<div class="view-embed">
    <div class="content-media">
    {let item=$object.data_map.item.content}
        <dl class="telemeta-item">
            <dt class="telemeta-sound">Sound:</dt>
            <dd class="telemeta-sound"><a href="{$item.mp3}">{$item.title|wash}</a></dd>

            <dt class="telemeta-duration">Duration:</dt>
            <dd class="telemeta-duration">
                <span class="telemeta-position">00:00:00</span>
                <span class="telemeta-separator"> / </span>
                {$item.duration_str}
            </dd>

            {if $item.description }
            <dt class="telemeta-description">Description:</dt>
            <dd class="telemeta-description">{$item.description}</dd>
            {/if}

            {if $item.creator }
            <dt class="telemeta-creator">Creator:</dt>
            <dd class="telemeta-creator">{$item.creator}</dd>
            {/if}

            {if $item.rights }
            <dt class="telemeta-rights">Legal rights:</dt>
            <dd class="telemeta-rights">{$item.rights}</dd>
            {/if}
        </dl>
    {/let}
    </div>
</div>

