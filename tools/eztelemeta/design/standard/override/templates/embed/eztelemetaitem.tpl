<script language="javascript">
soundManager.url = {'swf/'|ezdesign};
</script>
<div class="view-embed">
    <div class="content-media">
    {let attribute=$object.data_map.item}
        Telemeta Item:
        <dl>
        <dt>Server:</dt><dd>{$attribute.content.url}</dd>
        <dt>Identifier:</dt><dd>{$attribute.content.id}</dd>
        <dt>Title:</dt><dd>{$attribute.content.title|wash}</dd>
        </dl>
        <ul class="playlist">
        <li><a class="playable" href="{$attribute.content.mp3}">{$attribute.content.title|wash}</a></li>
        </ul>
    {/let}
    </div>
     <div id="control-template">
      <!-- control markup inserted dynamically after each link -->
      <div class="controls">
       <div class="statusbar">
        <div class="loading"></div>
         <div class="position"></div>
       </div>
      </div>
      <div class="timing">
       <div id="sm2_timing" class="timing-data">
        <span class="sm2_position">%s1</span> / <span class="sm2_total">%s2</span></div>
      </div>
      <div class="peak">
       <div class="peak-box"><span class="l"></span><span class="r"></span>
       </div>
      </div>
     </div>

     <div id="spectrum-container" class="spectrum-container">
      <div class="spectrum-box">
       <div class="spectrum"></div>
      </div>
     </div>
</div>

