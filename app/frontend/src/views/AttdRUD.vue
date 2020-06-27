<template>
  <div class="home">
    <b-table :items='attds'>
      <template v-slot:cell(actions)='row'>
        <b-button @click='deleterec(row)'> Delete </b-button>
        <b-button @click='updaterec(row)'> Update </b-button>
      </template>
    </b-table>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';

export default {
  name: 'AttdTable',
  props: {
    attds: Array,
  },
  methods: {
    updaterec(attddat) {
      this.$router.push({ name: 'AttdModify', params: { attd: attddat.item } });
    },
    deleterec(attddat) {
      const path = 'http://localhost:5000/attd/delete_attd_json';
      axios.post(path, attddat.item)
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
