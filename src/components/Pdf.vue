<template>
    <main>
        <aside>
            <button class="print-btn" @click="openPrintPreview" type="button">Print or Download as PDF</button>
            <div id="toc" v-if="config">
                <!-- <ul>
                    <li v-for="chapter in config.notebooks"> 
                        <a :href="`#${encodeURI(chapter)}`">{{ chapter }}</a>
                    </li>
                </ul> -->
            </div>
        </aside>
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
const doc = ref(new jsPDF({
    compress: true,
    orientation: 'p',
    unit: 'px',
    format: 'a4'
}));

const loadNotebooks = async () => {
    const configFile = await fetch('/nbconfig.json');
    config.value = await configFile.json();
    const notebooksNames = config.value.notebooks;
    for (let i = 0; i < notebooksNames.length; ++i) {
        const nb: string = notebooksNames[i];
        const file = await fetch(`/notebooks/${nb}.ipynb`);
        var json = await file.json();
        var rendered = ipynb2html.render(json);
        notebooks.value.push(rendered.outerHTML);
    }
};

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
