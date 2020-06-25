<template>
  <div id="modify-form">
    <form @submit.prevent="handle">
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
    handle() {
      this.$emit('updrec', this.moddept);
    },
  },
};
</script>
