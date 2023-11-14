// import * as language_dict from './assets/language_dict.json' // will not handle space key and delete key
import language_dict from './assets/language_dict.json'

let is_cn_broswer = (): boolean => {
    let language = window.navigator.language;
    if (language.startsWith("zh-")) {
        return true;
    }
    return false;
}

let to_title_case = (str: string) => {
  return str.replace(
    /\w\S*/g,
    function(txt) {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    }
  );
}

let translate_the_page = async () => {
    // console.log(language_dict)

    var all = document.getElementsByTagName("*");

    for (var i=0, max=all.length; i < max; i++) {
        let one_element = all[i]
        let old_text = one_element?.textContent
        if (old_text) {
            old_text = old_text.trim().toLowerCase()
            if (old_text in language_dict) {
                one_element.childNodes.forEach((node) => {
                    if (node.nodeValue) {
                        if (node.nodeValue.trim().toLowerCase() == old_text) {
                            let target_language_content = ""
                            if (is_cn_broswer()) {
                                //@ts-ignore
                                target_language_content = language_dict[old_text]['cn']
                            } else {
                                //@ts-ignore
                                target_language_content = to_title_case(language_dict[old_text]['en'])
                            }
                            node.nodeValue = target_language_content
                        }
                    }
                })
            }
        }
    }
}

export const start_the_translation = () => {
    translate_the_page()

    // do the translation when html change
    const config = { attributes: true, childList: true, subtree: true };

    // Callback function to execute when mutations are observed
    const callback = (mutationList: any, observer: any) => {
        mutationList
        observer
        translate_the_page()
    };

    // Create an observer instance linked to the callback function
    const observer = new MutationObserver(callback);

    // Start observing the target node for configured mutations
    observer.observe(document, config);
}
