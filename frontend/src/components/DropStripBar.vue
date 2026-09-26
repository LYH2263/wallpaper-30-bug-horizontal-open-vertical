<script setup>
defineProps({ drops: Number, dropLen: Number, rolls: Number, orientation: { type: String, default: 'vertical' } })
</script>
<template>
  <div class="strip-bar" :class="orientation === 'horizontal' ? 'horizontal' : 'vertical'">
    <div v-for="n in Math.min(drops || 0, 24)" :key="n" class="strip"
      :style="orientation === 'horizontal'
        ? { width: `${Math.min(240, (dropLen || 2) * 15)}px` }
        : { height: `${Math.min(120, (dropLen || 2) * 30)}px` }"></div>
    <p>共 {{ drops }} 条，约 {{ rolls }} 卷</p>
  </div>
</template>
