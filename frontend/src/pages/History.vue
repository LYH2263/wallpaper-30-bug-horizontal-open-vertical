<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
const items = ref([])
const openId = ref(null)
const detail = ref(null)
const err = ref('')
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
const orientLabel = (r) => r.result?.orientation === 'horizontal' ? '横贴' : '竖贴'
async function toggle(r) {
  err.value = ''
  if (openId.value === r.id) { openId.value = null; detail.value = null; return }
  openId.value = r.id
  detail.value = null
  // 详情与示意只认落库时钉住的那一版快照,不随系统默认贴向重算。
  try { detail.value = await getJSON(`/api/runs/${r.id}`) }
  catch (e) { err.value = '记录读取失败' }
}
</script>
<template>
  <div class="page"><h1>记录</h1>
  <ul>
    <li v-for="r in items" :key="r.id">
      <button class="link" @click="toggle(r)">#{{ r.id }}</button>
      {{ r.wall_name }} → {{ r.result?.rolls }} 卷 · {{ orientLabel(r) }} · {{ r.result?.drops }} 条
      · drop {{ r.result?.drop_len_m }}m · 每卷 {{ r.result?.strips_per_roll }} 条
      <div v-if="openId === r.id" class="run-detail">
        <p v-if="err" class="warn">{{ err }}</p>
        <template v-else-if="detail">
          <p>{{ detail.wall_name }} · {{ detail.roll_name }} —
            <strong>{{ detail.result.rolls }} 卷</strong> ·
            {{ detail.result.orientation === 'horizontal' ? '横贴' : '竖贴' }} ·
            {{ detail.result.drops }} 幅 · 条长 {{ detail.result.drop_len_m }}m ·
            每卷 {{ detail.result.strips_per_roll }} 条</p>
          <DropStripBar :drops="detail.result.drops" :drop-len="detail.result.drop_len_m"
            :rolls="detail.result.rolls" :orientation="detail.result.orientation" />
        </template>
      </div>
    </li>
  </ul>
  <p class="hint">编号详情、展开示意与列表摘要均为落库时钉住的同一版结果，不按系统默认贴向重跑。</p>
  </div>
</template>
