const { createApp } = Vue;

// 🔥 CHANGE THIS TO YOUR RENDER BACKEND URL
const API_BASE = "https://web-scraping-umzq.onrender.com";
// For local testing, use:
// const API_BASE = "http://localhost:5000";

createApp({
    data() {
        return {
            categories: [],
            selectedCategory: null,
            commodities: [],
            searchQuery: "",
            refreshInterval: null
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
            try {
                const res = await fetch(`${API_BASE}/categories`);
                const data = await res.json();

                this.categories = data;

                if (!this.selectedCategory && this.categories.length > 0) {
                    this.selectedCategory = this.categories[0];
                    await this.fetchCommodities();
                }
            } catch (error) {
                console.error("Error fetching categories:", error);
            }
        },

        async fetchCommodities() {
            if (!this.selectedCategory) return;

            try {
                const res = await fetch(
                    `${API_BASE}/commodities?category=${this.selectedCategory}&limit=100`
                );

                const data = await res.json();
                const newData = data.data;

                if (!newData) return;

                // First load
                if (this.commodities.length === 0) {
                    this.commodities = newData;
                    return;
                }

                // Update only price and pct
                newData.forEach(newItem => {
                    const existing = this.commodities.find(
                        item => item.commodity === newItem.commodity
                    );

                    if (existing) {
                        existing.price = newItem.price;
                        existing.pct = newItem.pct;
                    }
                });

            } catch (error) {
                console.error("Error fetching commodities:", error);
            }
        },

        selectCategory(cat) {
            this.selectedCategory = cat;
            this.fetchCommodities();
        }
    },

    mounted() {
        this.fetchCategories();

        // Prevent multiple intervals
        if (!this.refreshInterval) {
            this.refreshInterval = setInterval(() => {
                this.fetchCommodities();
            }, 30000);
        }
    },

    beforeUnmount() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
    }

}).mount("#app");
