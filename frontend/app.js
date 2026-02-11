const { createApp } = Vue;

createApp({
    data() {
        return {
            categories: [],
            selectedCategory: null,
            commodities: [],
            searchQuery: ""
        };
    },

    computed: {
        filteredCommodities() {
            if (!this.searchQuery) return this.commodities;

            return this.commodities.filter(item =>
                item.commodity.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        }
    },

    methods: {

        async fetchCategories() {
            const res = await fetch("http://localhost:5000/categories");
            this.categories = await res.json();

            if (!this.selectedCategory && this.categories.length > 0) {
                this.selectedCategory = this.categories[0];
                this.fetchCommodities();
            }
        },

        async fetchCommodities() {
            if (!this.selectedCategory) return;

            const res = await fetch(
                `http://localhost:5000/commodities?category=${this.selectedCategory}&limit=100`
            );

            const data = await res.json();
            const newData = data.data;

            // If first load → assign normally
            if (this.commodities.length === 0) {
                this.commodities = newData;
                return;
            }

            // Otherwise update ONLY price & pct
            newData.forEach(newItem => {
                const existing = this.commodities.find(
                    item => item.commodity === newItem.commodity
                );

                if (existing) {
                    existing.price = newItem.price;
                    existing.pct = newItem.pct;
                }
            });
        },

        selectCategory(cat) {
            this.selectedCategory = cat;
            this.fetchCommodities();
        }
    },

    mounted() {
        // Load categories once
        this.fetchCategories();

        // 🔥 Refresh ONLY card data every 30 seconds
        setInterval(() => {
            this.fetchCommodities();
        }, 30000);
    }

}).mount("#app");