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
import axios from 'axios';
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
    getAttd() {
      const path = 'http://localhost:5000/attd/check_attendance_json';
      console.log(path);
      axios.get(path)
        .then((res) => {
          this.attds = res.data.records;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getAttd();
  },
  updated() {
    this.getAttd();
  },
};
</script>
