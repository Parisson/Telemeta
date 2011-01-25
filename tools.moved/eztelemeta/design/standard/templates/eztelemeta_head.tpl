{if is_set( $module_result.content_info.persistent_variable.eztelemeta_player )}
<style type="text/css">
  @import url({"stylesheets/eztelemeta.css"|ezdesign});
</style>
<script language="JavaScript" type="text/javascript" src={"javascript/soundmanager2-nodebug-jsmin.js"|ezdesign}></script>
<script language="JavaScript" type="text/javascript" src={"javascript/eztelemeta-player.js"|ezdesign}></script>
<script language="JavaScript" type="text/javascript">
/* SoundManager2 configuration */
soundManager.url = {'swf/'|ezdesign};

telemetaPlayer = new TelemetaPlayer();

{literal}
soundManager.onload = function() {
    telemetaPlayer.setSoundManager(soundManager);
}
{/literal}
</script>
{/if}
