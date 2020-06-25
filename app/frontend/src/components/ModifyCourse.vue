<template>
  <div id="modify-form">
    <form @submit.prevent="handle">
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
    handle() {
      this.$emit('courseupd', this.modcourse);
    },
  },
};
</script>
