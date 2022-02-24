# Script to clean data and parse data back

import re

normalize_chars = {'Š': 'S', 'š': 's', 'Ð': 'D', 'Ž': 'Z', 'ž': 'z', 'À': 'A', 'Á': 'A', 'Â': 'A',
                   'Ã': 'A', 'Ä': 'A', 'Å': 'A', 'Æ': 'A', 'Ç': 'C', 'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
                   'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I', 'Ñ': 'N', 'Ń': 'N', 'Ò': 'O', 'Ó': 'O', 'Ô': 'O',
                   'Õ': 'O', 'Ö': 'O', 'Ø': 'O', 'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U', 'Ý': 'Y', 'Þ': 'B',
                   'ß': 'S', 'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a', 'æ': 'a', 'ç': 'c',
                   'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ð': 'o',
                   'ñ': 'n', 'ń': 'n', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ø': 'o', 'ù': 'u',
                   'ú': 'u', 'û': 'u', 'ü': 'u', 'ý': 'y', 'ý': 'y', 'þ': 'b', 'ÿ': 'y', 'ƒ': 'f', 'ă': 'a',
                   'î': 'i', 'â': 'a', 'ș': 's', 'ț': 't', 'Ă': 'A', 'Î': 'I', 'Â': 'A', 'Ș': 'S', 'Ț': 'T',
                   '“': '"', '”': '"', "’": "'"}
alphabets = """ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᵠᴿˢᵀᵁⱽᵂˣʸᶻ¹²³⁴⁵⁶⁷⁸⁹
ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ
₳฿₵ĐɆ₣₲ⱧłJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ₳฿₵ĐɆ₣₲ⱧłJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ
𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ
αв¢∂єfgнιנкℓмиσρqяѕтυνωχуzαв¢∂єfgнιנкℓмиσρqяѕтυνωχуz
ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ
𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ
𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅
ꪖꪉᨶᦔꫀᠻᦋꫝỉ᧒ƙꪶꪑ᭢ꪮᩏᧁꪹకᡶꪊꪜ᭙᥊ꪗɀꪖꪉᨶᦔꫀᠻᦋꫝỉ᧒ƙꪶꪑ᭢ꪮᩏᧁꪹకᡶꪊꪜ᭙᥊ꪗɀ
ᗩᗷᑕᗪᗴᖴǤᕼIᒎᛕᒪᗰᑎᗝᑭɊᖇᔕ丅ᑌᐯᗯ᙭Ƴ乙ᗩᗷᑕᗪᗴᖴǤᕼIᒎᛕᒪᗰᑎᗝᑭɊᖇᔕ丅ᑌᐯᗯ᙭Ƴ乙
🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿
абcдёfgнїjкгѫпѳpфя$тцѵщжчзАБCДЄFGHЇJКГѪЙѲPФЯ$TЦѴШЖЧЗ
🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩
𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩
𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵
αႦƈԃҽϝɠԋιʝƙʅɱɳσρϙɾʂƚυʋɯxყȥαႦƈԃҽϝɠԋιʝƙʅɱɳσρϙɾʂƚυʋɯxყȥ
ꍏ♭☾ᕲ€Ϝ❡♄♗♪ϰ↳ᗰ♫⊙ρᵠ☈∫†☋✓ω⌘⚧☡ꍏ♭☾ᕲ€Ϝ❡♄♗♪ϰ↳ᗰ♫⊙ρᵠ☈∫†☋✓ω⌘⚧☡
𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙
𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡
𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕
𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉
ǟɮƈɖɛʄɢɦɨʝӄʟʍռօքզʀֆȶʊʋաӼʏʐǟɮƈɖɛʄɢɦɨʝӄʟʍռօքզʀֆȶʊʋաӼʏʐ
ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ
ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ
🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉
ɐqɔpǝɟƃɥıɾʞlɯuodbɹsʇnʌʍxʎzɐqɔpǝɟƃɥıɾʞlɯuodbɹsʇnʌʍxʎz
ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴤᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴤᴛᴜᴠᴡxʏᴢ
🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉
λ𐒈𐒨Ꮷ𐒢ӺⳒ𐒅ᎥᏭᏥᏓ𐒄𐒐𐒀Ꮅ𐒉ⲄᎴᎿ𐒜ᏉᏊ𐒎𐒍೩λ𐒈𐒨Ꮷ𐒢ӺⳒ𐒅ᎥᏭᏥᏓ𐒄𐒐𐒀Ꮅ𐒉ᎿᎴⲄ𐒜ᏉᏊ𐒎𐒍೩
Ꮧ𐒈ᏣᏍᏋ೯Ꮾ𐒅𐒃ႰᏥႱ𐒄𐒐𐒀Ꭾ𐒛Ⲅ𐒡Ꮦ𐒜ᏉᏇ𐒓Ꮍ೩Ꮧ𐒈ᏣᏍᏋ೯Ꮾ𐒅𐒃ႰᏥႱ𐒄𐒐𐒀Ꭾ𐒛Ⲅ𐒡Ꮦ𐒜ᏉᏇ𐒓Ꮍ೩
ᏗᏰᏟᎴᏋӺᎶᏂᎥᏠᏦᏝᎷᏁᎧᎮᎤᏒᏕᏖᏬᏉᏇ೫Ꮍ೭ᏗᏰᏟᎴᏋӺᎶᏂᎥᏠᏦᏝᎷᏁᎧᎮᎤᏒᏕᏖᏬᏉᏇ೫Ꮍ೭
ᎯᏰᏟᏍᏋ೯ⳒᏲᎥႰᏥႱᎷႶᏫᎮᎤᏒᎴᎿᏪᏉᏇ೫Ꮍ೩ᎯᏰᏟᏍᏋ೯ⳒᏲᎥႰᏥႱᎷႶᏫᎮᎤᏒᎴᎿᏪᏉᏇ೫Ꮍ೩
ᏗᏰፈᎴᏋᎦᎶᏂᎥᏠᏦᏝᎷᏁᎧᎮᎤᏒᏕᏖᏬᏉᏇጀᎩፚᏗᏰፈᎴᏋᎦᎶᏂᎥᏠᏦᏝᎷᏁᎧᎮᎤᏒᏕᏖᏬᏉᏇጀᎩፚ
ΔβĆĐ€₣ǤĦƗĴҜŁΜŇØƤΩŘŞŦỮVŴЖ¥ŽΔβĆĐ€₣ǤĦƗĴҜŁΜŇØƤΩŘŞŦỮVŴЖ¥Ž
αɓ૮∂εƒɠɦเʝҡℓɱɳσρφ૨รƭµѵωאყƶαɓ૮∂εƒɠɦเʝҡℓɱɳσρφ૨รƭµѵωאყƶ
₳฿₡Đ€₣₲₶łɈ₭Ł₼₦Ꮻ₱₾₹$₮ɄṼ￦Ӿ¥₴₳฿₡Đ€₣₲₶łɈ₭Ł₼₦Ꮻ₱₾₹$₮ɄṼ￦Ӿ¥₴
ค๒ς๔єŦﻮђเןкl๓ภ๏קợгรtยשฬאꌦzค๒ς๔єŦﻮђเןкl๓ภ๏קợгรtยשฬאꌦz
คც८ძ૯Բ૭ҺɿʆқՆɱՈ૦ƿҩՐς੮υ౮ω૪ყઽคც८ძ૯Բ૭ҺɿʆқՆɱՈ૦ƿҩՐς੮υ౮ω૪ყઽ
ꋫꃲꉓꃸꑾꄘꁅꃄ꒐꒑ꀗ꒒ꂵꁹꄱꉣꋟꋪꇘ꓅ꌇ꒦ꅏꋋꌥ꒗ꋫꃲꉓꃸꑾꄘꁅꃄ꒐꒑ꀗ꒒ꂵꁹꄱꉣꋟꋪꇘ꓅ꌇ꒦ꅏꋋꌥ꒗
åβçď£ƒğȟȋjķȽɱñ¤קǭȑ§țɥ√Ψ×ÿžåβçď£ƒğȟȋjķȽɱñ¤קǭȑ§țɥ√Ψ×ÿž
ąβȼď€ƒǥhɨjЌℓʍɲ๏ρǭя$ţµ˅ώж¥ƶąβȼď€ƒǥhɨjЌℓʍɲ๏ρǭя$ţµ˅ώж¥ƶ
მჩეძპfცhἶქκlოῆõρგΓჰནυὗwჯყɀმჩეძპfცhἶქκlოῆõρგΓჰནυὗwჯყɀ
ÃβČĎẸƑĞĤĮĴЌĹϻŇỖƤǪŘŜŤǗϋŴЖЎŻÃβČĎẸƑĞĤĮĴЌĹϻŇỖƤǪŘŜŤǗϋŴЖЎŻ
ᗅᙘᑤᗫᙍᖴᘜᕼᓿᒙᖽᐸᒪᙢᘉᓎᕿᕴᖇSᖶᑗᐻᙎ᙭ᖻᙣᗅᙘᑤᗫᙍᖴᘜᕼᓿᒙᖽᐸᒪᙢᘉᓎᕿᕴᖇSᖶᑗᐻᙎ᙭ᖻᙣ
ꍏꌃꉓꀸꍟꎇꁅꃅꀤꀭꀘ꒒ꎭꈤꂦᖘꆰꋪꌗ꓄ꀎᐯꅏꊼꌩꁴꍏꌃꉓꀸꍟꎇꁅꃅꀤꀭꀘ꒒ꎭꈤꂦᖘꆰꋪꌗ꓄ꀎᐯꅏꊼꌩꁴ
ꁲꃳꏳꀷꑀꊯꁅꁝ꒐꒑ꈵ꒒ꂵꃔꊿꉣꋠꌅꈜꋖꌈ꒦ꅐꉤꐔꑒꁲꃳꏳꀷꑀꊯꁅꁝ꒐꒑ꈵ꒒ꂵꃔꊿꉣꋠꌅꈜꋖꌈ꒦ꅐꉤꐔꑒ
άвςȡέғģħίјķĻмήόρqŕşţùνώxчžάвςȡέғģħίјķĻмήόρqŕşţùνώxчž
ꋫꃃꏸꁕꍟꄘꁍꑛꂑꀭꀗ꒒ꁒꁹꆂꉣꁸ꒓ꌚ꓅ꐇꏝꅐꇓꐟꁴꋫꃃꏸꁕꍟꄘꁍꑛꂑꀭꀗ꒒ꁒꁹꆂꉣꁸ꒓ꌚ꓅ꐇꏝꅐꇓꐟꁴ
ДᏰℂ∂ƎƒᎶℍîʝƘℓℳИøρǪЯƧ✞υϑᏔ✘УՀДᏰℂ∂ƎƒᎶℍîʝƘℓℳИøρǪЯƧ✞υϑᏔ✘УՀ
ДБCDΞFGHIJҜLMИФPǪЯSΓЦVЩЖУZДБCDΞFGHIJҜLMИФPǪЯSΓЦVЩЖУZ
ǟɮƈɖɛʄɢɦɨʝᏦʟʍռօքզʀֆƭʊʋաxʏʐǟɮƈɖɛʄɢɦɨʝᏦʟʍռօքզʀֆƭʊʋաxʏʐ
ɑҍϲժҽƒցհíյƘӀʍղօԹզɾՏԵմѵա×վՀɑҍϲժҽƒցհíյƘӀʍղօԹզɾՏԵմѵա×վՀ
ꍏꌃꉓꀸꍟꎇꁅꃅꀤꀭꀘ꒒ꂵꈤꂦꉣꆰꋪꌗ꓄ꀎꃴꅏꊼꌩꁴꍏꌃꉓꀸꍟꎇꁅꃅꀤꀭꀘ꒒ꂵꈤꂦꉣꆰꋪꌗ꓄ꀎꃴꅏꊼꌩꁴ
ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᵟᴿˢᵀᵁᵛᵂˣᵞᶻᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᵟᴿˢᵀᵁᵛᵂˣᵞᶻ
ꋬꃳꉔ꒯ꏂꊰꍌꁝ꒐꒻ꀘ꒒ꂵꋊꄲꉣꆰꋪꇙ꓄꒤꒦ꅐꉧꌦꁴꋬꃳꉔ꒯ꏂꊰꍌꁝ꒐꒻ꀘ꒒ꂵꋊꄲꉣꆰꋪꇙ꓄꒤꒦ꅐꉧꌦꁴ
ΛϦㄈÐƐFƓнɪﾌҚŁ௱ЛØþҨ尺らŤЦƔƜχϤẔΛϦㄈÐƐFƓнɪﾌҚŁ௱ЛØþҨ尺らŤЦƔƜχϤẔ
ƛƁƇƊЄƑƓӇƖʆƘԼMƝƠƤƢƦƧƬƲƔƜҲƳȤƛƁƇƊЄƑƓӇƖʆƘԼMƝƠƤƢƦƧƬƲƔƜҲƳȤ
ꁲꋰꀯꂠꈼꄞꁅꍩꂑ꒻ꀗ꒒ꂵꋊꂦꉣꁷꌅꌚꋖꐇꀰꅏꇒꐞꁴꁲꋰꀯꂠꈼꄞꁅꍩꂑ꒻ꀗ꒒ꂵꋊꂦꉣꁷꌅꌚꋖꐇꀰꅏꇒꐞꁴ
ꋬꍗꏳꂟꏂꄟꍌꃬ꒐꒻ꀘ꒒ꂵꂚꉻꉣꋠꋪꑄ꓄ꀎ꒦ꅐꉼꐞꑓꋬꍗꏳꂟꏂꄟꍌꃬ꒐꒻ꀘ꒒ꂵꂚꉻꉣꋠꋪꑄ꓄ꀎ꒦ꅐꉼꐞꑓ
ԹՅՇԺȝԲԳɧɿʝƙʅʍՌԾρφՐՏԵՄ౮աՃՎՀԹՅՇԺȝԲԳɧɿʝƙʅʍՌԾρφՐՏԵՄ౮աՃՎՀ
ﾑ乃ᄃり乇ｷムんﾉﾌズﾚ爪刀のｱゐ尺丂ｲひ√山ﾒﾘ乙ﾑ乃ᄃり乇ｷムんﾉﾌズﾚ爪刀のｱゐ尺丂ｲひ√山ﾒﾘ乙
αßςdεƒghïյκﾚmη⊕pΩrš†u꒦ωxψzαßςdεƒghïյκﾚmη⊕pΩrš†u꒦ωxψz
ค๖¢໓ēfງhiวkl๓ຖ໐p๑rŞtนงຟxฯຊค๖¢໓ēfງhiวkl๓ຖ໐p๑rŞtนงຟxฯຊ
ąცƈɖɛʄɠɧıʝƙƖɱŋơ℘զཞʂɬų۷ῳҳყʑąცƈɖɛʄɠɧıʝƙƖɱŋơ℘զཞʂɬų۷ῳҳყʑ
ᗩᗷᑢᕲᘿᖴᘜᕼᓰᒚᖽᐸᒪᘻᘉᓍᕵᕴᖇSᖶᑘᐺᘺ᙭ᖻᗱᗩᗷᑢᕲᘿᖴᘜᕼᓰᒚᖽᐸᒪᘻᘉᓍᕵᕴᖇSᖶᑘᐺᘺ᙭ᖻᗱ
ꁲꃃꇃꂡꏹꄙꁍꀍꀤꀭꈵ꒒ꂵꋊꁏꉣꆰꋪꌚꋖꌈꃴꅐꋚꂖꁴꁲꃃꇃꂡꏹꄙꁍꀍꀤꀭꈵ꒒ꂵꋊꁏꉣꆰꋪꌚꋖꌈꃴꅐꋚꂖꁴ
ᕱც꒝Ꭰꂅꊰg♅ᎥϳКլოภԾᎵգᏒᏕϮuᏉᎳꊼᎩᏃᕱც꒝Ꭰꂅꊰg♅ᎥϳКլოภԾᎵգᏒᏕϮuᏉᎳꊼᎩᏃ
ልጌርዕቿቻኗዘጎጋጕረጠክዐየዒዪነፕሁሀሠሸሃጊልጌርዕቿቻኗዘጎጋጕረጠክዐየዒዪነፕሁሀሠሸሃጊ"""

for alphabet in alphabets[1:]:
    for ind, char in enumerate(alphabet.strip()):
        try:
            normalize_chars[char] = alphabets[0][ind]
        except Exception as e:
            print(e)
            print(alphabet, len(alphabet), len(alphabets[0]))
            break
normalize_chars.update({i: i for i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'})

normal_map = str.maketrans(normalize_chars)
del normalize_chars

# precompile regex
r2 = re.compile(r'https?: \/\/(?: www\.)?[-a-zA-Z0-9@: %._\+~#=\n]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?: [-a-zA-Z0-9()@: %_\+.~#?&\/=]*)|: [^\n\s]+?: |[\w\-\.]+@(?: [\w-]+\.)+[\w-]{2,4}|(?: \+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}|```.+?```\n?|(?: \\n)+|[^a-z0-9.,: ;%$&\'\"@!?\s\<\>\/\-\+\=\(\)\[\]*_]+|(?<=[a-z.,\': ;!?\/]) +(?=[.,\'!?\/])|([,\': ;\s\/\(\)\[\]\+\-\<\>\=])\1+|([_])\2{2,}|([a-z.!?*])\3{3,}|(: )(?: > (?: .*?)(?: \n+|\\n+|$))+', flags=re.DOTALL | re.IGNORECASE)  # noqa: E501
r3 = re.compile(r'[\U00003000\U0000205F\U0000202F\U0000200A\U00002000-\U00002009\U00001680\U000000A0\t]+| {2,}')  # noqa: E501
r4 = re.compile(r"([a-z1-9\'\"][\.\?\!\,])([a-z1-9\'\"])", re.IGNORECASE)  # noqa: E501


def clean(text):
    # handle special chars from other langs
    text = text.translate(normal_map)
    # remove urls, emails, code blocks, custom emojis,
    # non-emoji, punctuation, letters, and phone numbers
    text = re.sub(r2, r"\1\2\2\3\3\3\4", text.strip())
    # handle... interesting spaces
    text = re.sub(r3, " ", text.strip())
    text = re.sub(r4, r"\1 \2", text.strip())
    # handle newlines
    text = "/n".join([ln.strip().strip("\t") for ln in text.split("\n")])

    return text.lstrip(("-!.,^# ")).strip()


def parse(text):
    text = text.replace("/n", "\n")
    return text.lstrip(("-!.,^# ")).strip()
