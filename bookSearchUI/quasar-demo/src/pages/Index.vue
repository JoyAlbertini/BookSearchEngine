<template>
  <q-page class="flex">
    <div class="full-width">
      <books></books>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';
import Books from "components/Books";

export default defineComponent({
  name: 'PageIndex',
  components: {Books}
})
</script>
