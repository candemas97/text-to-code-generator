<template>
    <header>
        <h1 class="titulo">El generador Texto Código</h1>
    </header>
    <main>
        <textarea  v-model="query" />
        <div v-if="isFetching">Cargando</div>
        <div v-if="!isFetching && response.length > 0">{{ response }}</div>
        <button @click="requestModel">Execute</button>
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "App",
    data: function () {
        return {
            query: "",
            response: "",
            isFetching: false,
        };
    },
    methods: {
        async requestModel() {
            this.isFetching = true;
            const response = await fetch("http://localhost:8080/traslate-to-code", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    query: this.query,
                    idioma: "english",
                }),
            });
            const data = await response.json();
            this.response = data["generateCode"]
            console.log(data);
            this.isFetching = false;
        },
    },
});
</script>

<style scoped>
textarea {
    width: 60%;
    height: 10rem;
    resize: none;
}

</style>
