{if is_set( $module_result.content_info.persistent_variable.eztelemeta_player )}
<style type="text/css">
  @import url({"stylesheets/eztelemeta.css"|ezdesign});
  @import url({"stylesheets/page-player.css"|ezdesign});
</style>
  <script language="JavaScript" type="text/javascript" src={"javascript/soundmanager2.js"|ezdesign}></script>
  <script language="JavaScript" type="text/javascript">
    /* SoundManager2 configuration */
    soundManager.debugMode = true;
    soundManager.url = {'swf/'|ezdesign};

    /* SoundManager2 Page Player configuration */
    {literal}
    var PP_CONFIG = {
      flashVersion:     9,
      usePeakData:      true,
      useWaveformData:  false,
      useEQData:        false,
      useFavIcon:       false,
      useMovieStar:     false,
      updatePageTitle:  false
    }
    {/literal}
  </script>
  <script language="JavaScript" type="text/javascript" src={"javascript/page-player.js"|ezdesign}></script>
{/if}
