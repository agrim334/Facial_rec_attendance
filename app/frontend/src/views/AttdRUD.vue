<template>
  <div class="home">
    <table>
      <tr v-for='attd in attds' :key='attd.cid'>
        <AttdRecord :attd='attd' @updrec='updaterec' @delrec='deleterec'></AttdRecord>
      </tr>
    </table>
    <button id='add' @click='addrec'>Add attds</button>
  </div>

</template>

<script>
// @ is an alias to /src
import AttdRecord from '@/components/RUDAttd.vue';

export default {
  name: 'AttdTable',
  props: {
    attds: Array,
  },
  components: {
    AttdRecord,
  },
  methods: {
    updaterec(attddat) {
      alert(attddat);
    },
    deleterec(attddat) {
      alert(attddat);
    },
  },
};
</script>
