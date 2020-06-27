<template>
  <div class="home">
    <table>
      <tr v-for='attd in attds' :key='attd.cid'>
        <AttdRecord :attd='attd' @updrec='updaterec' @delrec='deleterec'></AttdRecord>
      </tr>
    </table>
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
      this.$router.push({ name: 'AttdModify', params: { attd: attddat } });
    },
    deleterec(attddat) {
      const path = 'http://localhost:5000/attd/delete_attd_json';
      axios.post(path, attddat)
        .then(() => {
          this.getAttd();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getAttd() {
      const path = 'http://localhost:5000/attd/check_attd_json';
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
};
</script>
