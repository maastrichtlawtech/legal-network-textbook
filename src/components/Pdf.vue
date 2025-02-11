<template>
    <main>
        <aside>
            <button class="print-btn" @click="openPrintPreview" type="button">Print or Download as PDF</button>
            <!-- TABLE OF CONTENTS -->
            <section id="toc" v-if="tocItems">
                <ul>
                    <template v-for="chapter in tocItems">
                        <li>
                            <a :href="`#${chapter[0].url}`">{{ chapter[0].label }}</a>
                            <ul>
                                <template v-for="(subchpater, index) in chapter">
                                    <li v-if="index > 0">
                                        <a :href="`#${subchpater.url}`">{{ subchpater.label }}</a>
                                    </li>
                                </template>
                            </ul>
                        </li>
                    </template>
                </ul>
            </section>
        </aside>
        <!-- NOTEBOOKS CONTENT -->
        <section id="notebooks-container">
            <div v-for="nb in notebooks">
                <div v-html="nb"></div>
            </div>
        </section>
    </main>
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue";
import { jsPDF } from "jspdf";
import "https://cdn.jsdelivr.net/npm/ipynb2html@0.4.0-rc.1/dist/ipynb2html-full.min.js";

// declare let html2pdf: any;
declare let ipynb2html: any;

const notebooks = ref<string[]>([]);
const config = ref();
const tocItems = ref<{label: string, url: string}[][]>([]);

// const doc = ref(new jsPDF({
//     compress: true,
//     orientation: 'p',
//     unit: 'px',
//     format: 'a4'
// }));

const loadNotebooks = async () => {
    const configFile = await fetch('/nbconfig.json');
    config.value = await configFile.json();
    const notebooksNames = config.value.notebooks;
    for (let i = 0; i < notebooksNames.length; ++i) {
        const nb: string = notebooksNames[i];
        const file = await fetch(`/notebooks/${nb}.ipynb`);
        var json = await file.json();
        var rendered = ipynb2html.render(json);
        addToToc(rendered);
        notebooks.value.push(rendered.outerHTML);
    }
};

const addToToc = (node: HTMLElement) => {

    if (node.tagName == 'H1') {
        tocItems.value.push([{ label: node.innerText, url: getUrl(node)}]);
    } else if (node.tagName == 'H2') {
        tocItems.value.at(-1).push({ label: node.innerText, url: getUrl(node)});
    }

    //TODO: upgrade for h3

    let child = node.firstChild;
    while (child) {
        addToToc(child as HTMLElement);
        child = child.nextSibling;
    }
};

function getUrl(node: HTMLElement) {
    let url = node.innerText.toLowerCase();
    url = url.replaceAll(/[^a-zA-Z0-9\s-:]/g, '');
    url = url.replaceAll(' ', '-');
    return url;
}

const openPrintPreview = () => {
    window.print();

    // const notebooksHTML = document.getElementById('notebooks-container');

    // doc.value.html(notebooksHTML!, {
    //     callback: (doc) => {
    //         doc.save("textbook.pdf");
    //     },
    //     html2canvas: { scale: .5 }
    // });
}

// const generatePDF = async () => {

//     const notebooksHTML = document.getElementById('notebooks-container');

//     // const options = {
//     //     filename: 'textbook.pdf',
//     //     image: { type: 'jpeg', quality: 0.7 },
//     //     // html2canvas: { scale: 1 },
//     //     jsPDF: { unit: 'px', format: 'a4', orientation: 'portrait', compress: true },
//     //     pagebreak: { mode: 'avoid-all' }
//     // };

//     // await html2pdf().from(notebooksHTML).set(options).save();

//     doc.value.html(notebooks.value[0], {
//         callback: (doc) => {
//             doc.save("textbook.pdf");
//         }
//     });
// };

onMounted(async () => {
    await loadNotebooks();
})
</script>
