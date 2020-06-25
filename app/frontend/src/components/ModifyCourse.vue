<template>
  <div id="modify-form">
    <form @submit.prevent="validate">
    <label>Course ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'modcourse.id'
    />
    <br>

    <label>Course name</label>
    <input type="text" placeholder = "Enter course name" v-model = 'modcourse.name'
    />
    <br>

    <input type="submit" value="Update Course" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'ModifyCourseForm',
  props: { courserec: Array },
  data() {
    return {
      modcourse: {
        id: this.courserec.id,
        name: this.courserec.name,
      },
    };
  },
  methods: {
    validate() {
      let f = 0;
      if (this.modcourse.id === null || this.modcourse.id === '') {
        alert('fill course id');
        f = 1;
      }
      if (this.modcourse.name === null || this.modcourse.name === '') {
        alert('fill course name');
        f = 1;
      }
      if (f === 0) {
        this.$emit('courseupd', this.modcourse);
      }
    },
  },
};
</script>
