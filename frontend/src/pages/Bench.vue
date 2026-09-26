<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
const walls = ref([]); const rolls = ref([]); const wallId = ref(1); const rollId = ref(1); const out = ref(null)
const orientation = ref('vertical'); const err = ref('')
onMounted(async () => {
  walls.value = (await getJSON('/api/walls')).items.filter(w => w.data_quality==='clean')
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality==='clean')
  if (walls.value.length) wallId.value = walls.value[0].id
  if (rolls.value.length) rollId.value = rolls.value[0].id
  const s = await getJSON('/api/settings')
  if (s.default_orientation) orientation.value = s.default_orientation
})
async function run(save) {
  err.value = ''
  try {
    out.value = save
      ? await postJSON('/api/estimate', { wall_id: wallId.value, roll_id: rollId.value, save: true, orientation: orientation.value })
      : await getJSON(`/api/estimate?wall_id=${wallId.value}&roll_id=${rollId.value}&orientation=${orientation.value}`)
  } catch (e) { err.value = '测算被拒绝：请检查幅宽/卷长是否有效' }
}
watch(orientation, () => { if (out.value) run(false) })
</script>
<template>
  <div class="page"><h1>算卷工作台</h1>
  <select v-model.number="wallId"><option v-for="w in walls" :key="w.id" :value="w.id">{{ w.name }}</option></select>
  <select v-model.number="rollId"><option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option></select>
  <label><input type="radio" value="vertical" v-model="orientation" /> 竖贴</label>
  <label><input type="radio" value="horizontal" v-model="orientation" /> 横贴</label>
  <button @click="run(false)">试算</button><button @click="run(true)">保存</button>
  <p v-if="err" class="warn">{{ err }}</p>
  <div v-if="out"><strong>{{ out.rolls }} 卷</strong> · {{ out.drops }} 条 · 每条 {{ out.drop_len_m }}m · {{ out.orientation === 'horizontal' ? '横贴' : '竖贴' }}
  <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" :orientation="out.orientation" /></div>
  </div>
</template>
