/** herre tools or functions mainly copied and modified from internet which might be useful
 * THIS SCRIPT IS NOT LOADED IN ANY PAGE, WE JUST WANT TO COLLECT HERE FUNCTION UTILITIES WHICH ARE NOT USED ANYMORE, BUT WHICH MIGHT
 * BE USEFUL AGAIN
 */
var temp_utilitites = {

    /**
     * old function used to assess span width. We calculate the width of a span niw, to be more sure
     */
    textWidth : function(text, fontSize) {
        var ratio = 3/5;
        return text.length * ratio * fontSize;
    },

    //css specific functions:
    //get computed style first (cross browser solution, from http://blog.stchur.com/2006/06/21/css-computed-style/
    getComputedStyle : function(_elem, _style){
        var computedStyle;
        var $J = this.$J;
        if(_elem instanceof $J){ //note: '_elem instanceof this.$J' doesnt work. why??
            _elem = _elem.get(0);
        }
        if (typeof _elem.currentStyle != 'undefined'){
            computedStyle = _elem.currentStyle;
        }else{
            computedStyle = document.defaultView.getComputedStyle(_elem, null);
        }
        return computedStyle[_style];
    },
    //returns a hex color from strColor. strColor can be one of the predefined css colors (eg, 'aliceBlue', case insensitive)
    //or rgb (eg: rgb(12,0,45)) or an hex color (eg, '#ff98a3' or '#f8g'). Leading and trailing spaces will be omitted,
    //case is insensitive, an empty string is returned in case of error (bad format string, parseInt errors etcetera..)
    color : function(strColor){
        if(!strColor){
            return '';
        }
        strColor = strColor.replace(/(^\s+|\s+$)/g,'').toLowerCase();
        if(!strColor){
            return '';
        }
        var predefined_colors = {
            aliceblue:"#f0f8ff",
            antiquewhite:"#faebd7",
            aqua:"#00ffff",
            aquamarine:"#7fffd4",
            azure:"#f0ffff",
            beige:"#f5f5dc",
            bisque:"#ffe4c4",
            black:"#000000",
            blanchedalmond:"#ffebcd",
            blue:"#0000ff",
            blueviolet:"#8a2be2",
            brown:"#a52a2a",
            burlywood:"#deb887",
            cadetblue:"#5f9ea0",
            chartreuse:"#7fff00",
            chocolate:"#d2691e",
            coral:"#ff7f50",
            cornflowerblue:"#6495ed",
            cornsilk:"#fff8dc",
            crimson:"#dc143c",
            cyan:"#00ffff",
            darkblue:"#00008b",
            darkcyan:"#008b8b",
            darkgoldenrod:"#b8860b",
            darkgray:"#a9a9a9",
            darkgrey:"#a9a9a9",
            darkgreen:"#006400",
            darkkhaki:"#bdb76b",
            darkmagenta:"#8b008b",
            darkolivegreen:"#556b2f",
            darkorange:"#ff8c00",
            darkorchid:"#9932cc",
            darkred:"#8b0000",
            darksalmon:"#e9967a",
            darkseagreen:"#8fbc8f",
            darkslateblue:"#483d8b",
            darkslategray:"#2f4f4f",
            darkslategrey:"#2f4f4f",
            darkturquoise:"#00ced1",
            darkviolet:"#9400d3",
            deeppink:"#ff1493",
            deepskyblue:"#00bfff",
            dimgray:"#696969",
            dimgrey:"#696969",
            dodgerblue:"#1e90ff",
            firebrick:"#b22222",
            floralwhite:"#fffaf0",
            forestgreen:"#228b22",
            fuchsia:"#ff00ff",
            gainsboro:"#dcdcdc",
            ghostwhite:"#f8f8ff",
            gold:"#ffd700",
            goldenrod:"#daa520",
            gray:"#808080",
            grey:"#808080",
            green:"#008000",
            greenyellow:"#adff2f",
            honeydew:"#f0fff0",
            hotpink:"#ff69b4",
            indianred:"#cd5c5c",
            indigo:"#4b0082",
            ivory:"#fffff0",
            khaki:"#f0e68c",
            lavender:"#e6e6fa",
            lavenderblush:"#fff0f5",
            lawngreen:"#7cfc00",
            lemonchiffon:"#fffacd",
            lightblue:"#add8e6",
            lightcoral:"#f08080",
            lightcyan:"#e0ffff",
            lightgoldenrodyellow:"#fafad2",
            lightgray:"#d3d3d3",
            lightgrey:"#d3d3d3",
            lightgreen:"#90ee90",
            lightpink:"#ffb6c1",
            lightsalmon:"#ffa07a",
            lightseagreen:"#20b2aa",
            lightskyblue:"#87cefa",
            lightslategray:"#778899",
            lightslategrey:"#778899",
            lightsteelblue:"#b0c4de",
            lightyellow:"#ffffe0",
            lime:"#00ff00",
            limegreen:"#32cd32",
            linen:"#faf0e6",
            magenta:"#ff00ff",
            maroon:"#800000",
            mediumaquamarine:"#66cdaa",
            mediumblue:"#0000cd",
            mediumorchid:"#ba55d3",
            mediumpurple:"#9370d8",
            mediumseagreen:"#3cb371",
            mediumslateblue:"#7b68ee",
            mediumspringgreen:"#00fa9a",
            mediumturquoise:"#48d1cc",
            mediumvioletred:"#c71585",
            midnightblue:"#191970",
            mintcream:"#f5fffa",
            mistyrose:"#ffe4e1",
            moccasin:"#ffe4b5",
            navajowhite:"#ffdead",
            navy:"#000080",
            oldlace:"#fdf5e6",
            olive:"#808000",
            olivedrab:"#6b8e23",
            orange:"#ffa500",
            orangered:"#ff4500",
            orchid:"#da70d6",
            palegoldenrod:"#eee8aa",
            palegreen:"#98fb98",
            paleturquoise:"#afeeee",
            palevioletred:"#d87093",
            papayawhip:"#ffefd5",
            peachpuff:"#ffdab9",
            peru:"#cd853f",
            pink:"#ffc0cb",
            plum:"#dda0dd",
            powderblue:"#b0e0e6",
            purple:"#800080",
            red:"#ff0000",
            rosybrown:"#bc8f8f",
            royalblue:"#4169e1",
            saddlebrown:"#8b4513",
            salmon:"#fa8072",
            sandybrown:"#f4a460",
            seagreen:"#2e8b57",
            seashell:"#fff5ee",
            sienna:"#a0522d",
            silver:"#c0c0c0",
            skyblue:"#87ceeb",
            slateblue:"#6a5acd",
            slategray:"#708090",
            slategrey:"#708090",
            snow:"#fffafa",
            springgreen:"#00ff7f",
            steelblue:"#4682b4",
            tan:"#d2b48c",
            teal:"#008080",
            thistle:"#d8bfd8",
            tomato:"#ff6347",
            turquoise:"#40e0d0",
            violet:"#ee82ee",
            wheat:"#f5deb3",
            white:"#ffffff",
            whitesmoke:"#f5f5f5",
            yellow:"#ffff00",
            yellowgreen:"#9acd32"
        };
        var cl = predefined_colors[strColor];
        if(cl){
            return cl;
        }
        var pint = parseInt;
        //color parsers: note that the order is not random: we put first the most likely case ('#aaaaaa') and at last
        //the less one ('rgb(...)'), this might increase performances in most cases, especially if this method is called from
        //within a loop
        var color_defs = [
        {
            re: /^#*(\w{2})(\w{2})(\w{2})$/, //example: ['#00ff00', '336699'],
            process: function (bits){
                return [pint(bits[1], 16),pint(bits[2], 16),pint(bits[3], 16)];
            }
        },

        {
            re: /^#*(\w{1})(\w{1})(\w{1})$/, //example: ['#fb0', 'f0f'],
            process: function (bits){
                return [pint(bits[1] + bits[1], 16),pint(bits[2] + bits[2], 16),pint(bits[3] + bits[3], 16)];
            }
        },
        {
            re: /^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$/, //example: ['rgb(123, 234, 45)', 'rgb(255,234,245)'],
            process: function (bits){
                return [pint(bits[1]), pint(bits[2]),pint(bits[3])];
            }
        }

        ];

        // search through the definitions to find a match
        var nan = isNaN;
        for (var i = 0; i < color_defs.length; i++) {
            var re = color_defs[i].re;
            var processor = color_defs[i].process;
            var bits = re.exec(strColor);
            if (bits) {
                var channels = processor(bits);
                if(channels.length ==3){
                    for(var j=0; j<3; j++){
                        var c = channels[j];
                        c = (nan(c) || c< 0 ? 0 : (c>255 ? 255 :c));
                        c = c.toString(16);
                        var len = c.length;
                        switch(len){
                            case 1:
                                c = '0'+c;
                                break;
                            case 2:
                                break;
                            default:
                                return '';
                        }
                        channels[j] = c;
                    }
                    return '#'+channels.join('');
                }
            }
        }
        return '';
    }
}