<template>
  <h1 class="titulo">El generador Texto Código</h1>
  <InputQuery :prop1="varApp" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import InputQuery from "./components/InputQuery.vue";

export default defineComponent({
  name: "App",
  components: { InputQuery },
  data: function () {
    return {
        varApp: "pene"
    };
  },
});
</script>

<style scoped>
/* h1 {
  color: "red";
} */
</style>
