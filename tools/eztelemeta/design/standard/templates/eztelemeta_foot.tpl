{if is_set( $module_result.content_info.persistent_variable.eztelemeta_player )}
   <div id="ezt-control-template">
    <!-- control markup inserted dynamically after each link -->
    <div class="ezt-controls">
     <div class="ezt-statusbar">
      <div class="ezt-loading"></div>
       <div class="ezt-position"></div>
     </div>
    </div>
    <div class="ezt-timing">
     <div id="ezt-sm2_timing" class="ezt-timing-data">
      <span class="ezt-sm2_position">%s1</span> / <span class="ezt-sm2_total">%s2</span></div>
    </div>
    <div class="ezt-peak">
     <div class="ezt-peak-box"><span class="ezt-l"></span><span class="ezt-r"></span>
     </div>
    </div>
   </div>

   <div id="ezt-spectrum-container" class="ezt-spectrum-container">
    <div class="ezt-spectrum-box">
     <div class="ezt-spectrum"></div>
    </div>
   </div>
{/if}
