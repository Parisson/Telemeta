{eztelemetadata_set('eztelemeta_player', true)}
{def $item=$attribute.content}
<div class="telemeta-item">
    <dl>
        <dt class="telemeta-sound">{'Sound'|i18n('eztelemeta')} :</dt>
        <dd class="telemeta-sound"><a href="{$item.mp3}">{$item.title|wash}</a></dd>

        <dt class="telemeta-duration">{'Duration'|i18n('eztelemeta')} :</dt>
        <dd class="telemeta-duration">
            <span class="telemeta-position">00:00:00</span>
            <span class="telemeta-separator"> / </span>
            {$item.duration_str}
        </dd>

        {if $item.description }
        <dt class="telemeta-description">{'Description'|i18n('eztelemeta')} :</dt>
        <dd class="telemeta-description">{$item.description|wash}</dd>
        {/if}

        {if $item.creator }
        <dt class="telemeta-creator">{'Creator'|i18n('eztelemeta')} :</dt>
        <dd class="telemeta-creator">{$item.creator|wash}</dd>
        {/if}

        {if $item.rights }
        <dt class="telemeta-rights">{'Legal rights'|i18n('eztelemeta')} :</dt>
        <dd class="telemeta-rights">{$item.rights|wash}</dd>
        {/if}
    </dl>
    <div class="telemeta-clear"></div>
</div>
{undef}
