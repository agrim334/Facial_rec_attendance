<template>
  <div class="home">
    <table>
      <tr v-for='dept in depts' :key='dept.id'>
        <deptrec :dept='dept' @updrec='updaterec' @delrec='deleterec'></deptrec>
      </tr>
    </table>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import deptrec from '@/components/RUDDept.vue';

export default {
  name: 'DeptTable',
  props: {
    depts: Array,
  },
  components: {
    deptrec,
  },
  data() {
    return {
      deptrecarr: Array,
    };
  },
  methods: {
    updaterec(deptdat) {
      this.$router.push({ name: 'DeptModify', params: { dept: deptdat } });
    },
    deleterec(deptdat) {
      const path = 'http://localhost:5000/dept/delete_dept_json';
      axios.post(path, deptdat.id)
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
