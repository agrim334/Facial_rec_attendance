<template>
  <div id="modify-form">
    <form @submit.prevent="validate">
    <label>dept ID</label>
    <input type="text" placeholder = "Enter Department ID" v-model = 'moddept.id'
     />
    <br>

    <label>dept name</label>
    <input type="text" placeholder = "Enter Deptartment name" v-model = 'moddept.name'
    />
    <br>

    <input type="submit" value="Update dept" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'ModifyDeptForm',
  props: { deptrec: Array },
  data() {
    return {
      moddept: {
        id: this.deptrec.id,
        name: this.deptrec.name,
      },
    };
  },
  methods: {
    validate() {
      let f = 0;
      if (this.dept.id === null || this.dept.id === '') {
        alert('fill dept id');
        f = 1;
      }
      if (this.dept.name === null || this.dept.name === '') {
        alert('fill dept name');
        f = 1;
      }
      if (f === 0) {
        this.$emit('updrec', this.moddept);
      }
    },
  },
};
</script>
