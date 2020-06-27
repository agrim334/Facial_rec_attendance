<template>
  <div class="home">
    <b-table :items='depts'>
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
  name: 'DeptTable',
  props: {
    depts: Array,
  },
  methods: {
    updaterec(deptdat) {
      this.$router.push({ name: 'DeptModify', params: { dept: deptdat.item } });
    },
    deleterec(deptdat) {
      const path = 'http://localhost:5000/dept/delete_dept_json';
      axios.post(path, deptdat.item.id)
        .then(() => {
          this.getDept();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getDept() {
      const path = 'http://localhost:5000/dept/check_dept_json';
      axios.get(path)
        .then((res) => {
          this.depts = res.data.records;
          for (let i = 0; i < this.depts.length; i += 1) {
            this.depts[i].actions = '';
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getDept();
  },
};
</script>
