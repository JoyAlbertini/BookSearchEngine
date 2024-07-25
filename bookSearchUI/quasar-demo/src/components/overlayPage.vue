<template>
<div class="overlay full-width full-height">
  <p>text</p>
</div>
</template>

<script>
export default {
  name: "overlayPage"
}
</script>

<style scoped>

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0.3;
  background-color: black;
  z-index: 0;
}
</style>
