<template>
    <div id="pdf-container" class="mx-auto container">
        <div v-for="nb in notebooks">
            <div v-html="nb"></div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue";
import "https://cdn.jsdelivr.net/npm/ipynb2html@0.4.0-rc.1/dist/ipynb2html-full.min.js";

declare let ipynb2html: any;
const notebooks = ref<string[]>([]);

const loadNotebooks = async () => {
    const configFile = await fetch('/nbconfig.json');
    const config = await configFile.json();
    const notebooksNames = config.notebooks;
    for(let i = 0; i < notebooksNames.length; ++i) {
        const nb: string = notebooksNames[i];
        const file = await fetch(`/notebooks/${nb}.ipynb`);
        var json = await file.json();
        var rendered = ipynb2html.render(json);
        notebooks.value.push(rendered.outerHTML);
    }
};

onMounted(async () => {
    await loadNotebooks();
})
</script>
<style scoped>
@import url('https://cdn.jsdelivr.net/npm/ipynb2html@0.4.0-rc.1/dist/notebook.min.css');
@import url('https://cdn.jsdelivr.net/npm/katex@0.16.3/dist/katex.min.css');
@import url('https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.7.3/build/styles/default.min.css');
</style>
