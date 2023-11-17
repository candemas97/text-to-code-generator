<template>
  <input v-model="prop1" />
  <p>
    {{ prop1 }} {{ prop2 }}
  </p>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "InputQuery",
  props: {
    prop1: { type: String, required: true },
    prop2: { type: Number, required: false, default: 5 },
  },
  data: function () {
    return {
      miVariable: "",
    };
  },
});
</script>

<style></style>
