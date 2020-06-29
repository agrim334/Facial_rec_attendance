<template>
  <div class="home">
    <AttdRecord :attds='attds' @updrec='updaterec' @delrec='deleterec'>
    </AttdRecord>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import AttdRecord from '../components/RUDAttd.vue';

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
      const path = 'attd/delete_attd_json';
      this.$store.dispatch('authrequest', { url: path, data: attddat })
        .then(() => {
          this.getAttd();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getAttd() {
      const path = 'attd/check_attd_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((res) => {
          this.attds = res.data.records;
          for (let i = 0; i < this.attds.length; i += 1) {
            this.attds[i].actions = '';
          }
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
