import tensorflow as tf
import numpy as np
import pandas as pd
import streamlit as st
import requests
import random
from deep_translator import GoogleTranslator
from PIL import Image
# Language support
selected_language = st.sidebar.selectbox("🌍 Choose Language", ["English", "Telugu"])
def translate_text(text):
    try:
        if selected_language == "Telugu":
            return GoogleTranslator(source="auto", target="te").translate(text)
        return text
    except Exception as e:
        st.error(f"Translation Error: {e}")
        return text
def model_prediction(test_image):
    try:
        # Load the trained model
        model = tf.keras.models.load_model("trained_plant_disease_model.keras")
        # Process the uploaded image
        image = Image.open(test_image).convert("RGB")  # Convert to RGB
        image = image.resize((128, 128))  # Resize to match model input
        input_arr = np.array(image)  # Convert image to array
        input_arr = np.expand_dims(input_arr, axis=0)  # Convert to batch format
        predictions = model.predict(input_arr)
        result_index = np.argmax(predictions)  # Get highest confidence prediction
        confidence = np.max(predictions) * 100  # Convert to percentage
        return result_index, confidence
    except Exception as e:
        st.error(f"Model Prediction Error: {e}")
        return None, None
# Sidebar Navigation
st.sidebar.title((" Tomato Leaf Disease Detection System"))
page = st.sidebar.radio(("Navigation"), [("Home"), ("Disease Detection"), ("Tomato Care Guide"), ("Chatbot")])
# Home Page
if page == translate_text("Home"):
    st.markdown(f"<h1 style='text-align: center;'>{translate_text('Tomato Leaf Disease Detection System')}</h1>", unsafe_allow_html=True)
    st.image("Diseases.png", use_container_width=True)
    st.markdown(translate_text("""
    ## About this System
    This AI-powered system helps in detecting tomato leaf diseases, providing organic solutions, and offering care tips. 
    **Features:**
    - Disease detection through image upload
    - Organic remedies for tomato leaf diseases
    - Comprehensive tomato care guide
    - Chatbot for FAQs
    """))
# Prediction Page
elif page == "Disease Detection":
    st.header(translate_text("Upload a Plant Leaf Image"))
    test_image = st.file_uploader("Choose an Image:", type=["jpg", "png", "jpeg"])
    if test_image:
        st.image(test_image, caption="Uploaded Image", use_column_width=True)
        if st.button("Predict"):
            with st.spinner(" Analyzing Image... Please wait."):
                result_index, confidence = model_prediction(test_image)
            class_labels = [
                'Tomato Bacterial Spot', 'Tomato  Early blight','Tomato Healthy', 'Tomato Late Blight','Tomato Leaf Mold','Tomato Septoria leaf Spot'
                'Tomato Spider Mites','Tomato Target Spot', 'Tomato Mosaic Virus', 'Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___healthy'
            ]
            if result_index is not None and 0 <= result_index < len(class_labels):
                predicted_disease = class_labels[result_index]
                st.success(f"✅ {translate_text('Model Prediction')}: {translate_text(predicted_disease)} ({confidence:.2f}% Confidence)")
                # Load fertilizer and pesticide recommendations
                df_path = "C:/project/Leaf Disease Detection/tomato_disease_guide_detailed.csv"
                try:
                    df = pd.read_csv(df_path)
                except FileNotFoundError:
                    st.error(f"Error: The file {df_path} was not found.")
                    df = pd.DataFrame()
                except Exception as e:
                    st.error(f"Error loading CSV file: {e}")
                    df = pd.DataFrame()
                # Fetch disease info from the CSV file
                disease_info = df[df["Disease"] == predicted_disease]
                if not disease_info.empty:
                    disease_info = disease_info.iloc[0]
                    st.info(f"🌿 {translate_text('Symptoms')}: {translate_text(str(disease_info['Symptoms']))}")
                    st.warning(f"🐞 {translate_text('Organic Pesticides')}: {translate_text(str(disease_info['Organic Pesticides']))}")
                    st.success(f"💡 {translate_text('Tips')}: {translate_text(str(disease_info['Tips']))}")
                    # Allow users to download the report
                    report_text = (
                        f"Disease: {predicted_disease}\n"
                        f"Fertilizer: {disease_info['Symptoms']}\n"
                        f"Pesticide: {disease_info['Organic Pesticides']}\n"
                        f"Tips: {disease_info['Tips']}"
                    )
                    st.download_button(label=translate_text("📄 Download Report"), data=report_text, file_name="plant_disease_report.txt")
                else:
                    st.error(f"It's not a tomato,It's a: {predicted_disease},can i suggest a pesticide for only a Tomato leaf diseases.")
            else:
                st.error("Upload a Tomato leaf with a clarity.It's not clear tomato leaf image so model could not make a valid prediction. Please try again with clear image.")
# Tomato Care Guide Page
elif page == "Tomato Care Guide":
    st.markdown("## 🌿 Tomato Care Guide")
    with st.expander("🍅 Types of Tomatoes"):
        st.markdown("""
        **Determinate (Bush type):**
        - Grow to a fixed height and produce fruit all at once.
        - Ideal for container gardening.
        **Indeterminate (Vining type):**
        - Continue growing and producing fruit throughout the season.
        - Require staking or other support. 
        **Recommended Disease-Resistant Varieties:**
        - Cherry Tomatoes  
        - Roma Tomatoes 
        - Brandywine (Heirloom) 
        - San Marzano 🇮🇹
        """)
    with st.expander("🌱 Soil Preparation"):
        st.markdown("""
Preparing the soil properly is crucial for cultivating healthy tomato plants and achieving a bountiful harvest. Here's a comprehensive guide on soil preparation for tomato cultivation:
1. Soil Testing and pH Adjustment
Begin by testing the soil to determine its pH and nutrient levels. Tomatoes thrive in slightly acidic to neutral soil with a pH between 6.5 and 7.0. Adjust the pH accordingly:
•	To Raise pH (Reduce Acidity): Incorporate lime into the soil.
•	To Lower pH (Increase Acidity): Add sulfur or organic materials like pine needles.
Soil testing kits are available, or local agricultural extensions can provide this service.
2. Enhancing Soil Fertility with Organic Matter
Integrate organic matter to improve soil structure, fertility, and moisture retention:
•	Compost: Apply a 2-inch layer of compost over the planting area and mix it into the top 6 inches of soil. 
•	Aged Manure: Use well-rotted manure to enrich the soil, ensuring it's free from herbicides that could harm tomato plants. 
3. Deep Soil Preparation
Tomato roots penetrate deeply; thus, thorough soil preparation is essential:
•	Tilling: Loosen the soil to a depth of 12 inches to promote root growth and drainage. 
•	Incorporating Amendments: While tilling, mix in compost or aged manure to enhance soil fertility.
4. Ensuring Proper Drainage
Tomatoes require well-draining soil to prevent root diseases:
•	Soil Texture: Amend heavy clay soils with compost to improve drainage. 
•	Raised Beds: Consider planting tomatoes in raised beds filled with quality soil to ensure adequate drainage. 
5. Crop Rotation Practices
To minimize soil-borne diseases:
•	Rotation: Avoid planting tomatoes in the same location each year. Implement a three-year crop rotation plan, alternating with non-solanaceous crops. 
6. Mulching Strategies
Mulching offers multiple benefits:
•	Organic Mulch: Apply a 2-inch layer of organic mulch, such as shredded bark or grass clippings, around tomato plants to conserve moisture, suppress weeds, and enrich the soil as it decomposes. 
7. Cover Crops for Soil Health
Planting cover crops during the off-season can enhance soil fertility:
•	Green Manure: Grow cover crops like winter rye or annual ryegrass and incorporate them into the soil before planting tomatoes to boost organic matter and nutrient content. 
8. Avoiding Soil Contaminants
Ensure the planting area is free from harmful substances:
•	Site Selection: Avoid areas near black walnut trees, as they release juglone, which is toxic to tomatoes. 
9. Continuous Soil Monitoring
Regularly assess soil health:
•	Soil Testing: Periodically test soil to monitor pH and nutrient levels, making adjustments as needed to maintain optimal conditions for tomato growth. 
By following these detailed soil preparation steps, farmers can create an optimal environment for tomato plants, leading to robust growth and abundant yields.""")
    with st.expander("☀️ Temperature & Climate"):
        st.markdown("""
        Understanding the optimal temperature and climate conditions is crucial for successful tomato cultivation. Here's a detailed guide to assist farmers:
1. Optimal Temperature Ranges
•	Germination: Tomato seeds germinate best at soil temperatures between 18-29°C (65-85°F). 
•	Daytime Growth: The ideal daytime temperature for tomato plants is between 21-27°C (70-82°F). 
•	Nighttime Growth: Nighttime temperatures should ideally range from 16-18°C (62-64°F). 
2. Temperature Tolerances
•	Minimum Threshold: Tomato plants can tolerate minimum temperatures around 10°C (50°F), but growth may be stunted if exposed to such lows for extended periods. 
•	Maximum Threshold: Temperatures above 34°C (93°F) can adversely affect tomato plants, leading to issues like blossom drop and reduced fruit set. 
3. Soil Temperature for Transplanting
•	Transplanting: Ensure soil temperatures have warmed to about 15.5°C (60°F) before setting tomatoes into the garden. 
4. Impact of Temperature Extremes
•	Low Temperatures: Exposure to temperatures below 10°C (50°F) can cause chilling injury, leading to delayed growth and potential crop loss.
•	High Temperatures: Prolonged periods above 32°C (90°F) can impair pollination, resulting in poor fruit set and quality.
5. Climate Considerations
•	Humidity: Moderate humidity levels are ideal. High humidity can promote fungal diseases, while low humidity may cause issues like blossom end rot.
•	Rainfall: Consistent moisture is essential, but waterlogged conditions should be avoided to prevent root diseases.
•	Sunlight: Tomatoes require full sun, ideally 6-8 hours daily, for optimal growth and fruit development.
6. Regional Adaptations
•	Cooler Climates: In regions with shorter growing seasons, select early-maturing and cold-tolerant tomato varieties.
•	Warmer Climates: Choose heat-tolerant varieties that can set fruit even in high temperatures.
By adhering to these temperature and climate guidelines, farmers can optimize tomato growth, leading to healthier plants and higher yields.""")
    with st.expander("👩‍🌾 Planting Tomatoes"):
        st.markdown("""
        Proper planting techniques are essential for successful tomato cultivation. Here's a detailed guide to assist farmers:
1. Selecting the Right Location
•	Sunlight: Tomatoes require full sun, ideally 6 to 8 hours of direct sunlight daily, for optimal growth and fruit development. 
•	Soil Quality: Plant tomatoes in rich, well-drained soil with a slightly acidic to neutral pH (6.0 to 7.0). 
2. Preparing the Soil
•	Soil Testing: Conduct a soil test to determine nutrient levels and pH. Amend the soil based on test results to ensure it meets the necessary conditions for tomato growth.
•	Organic Matter: Incorporate compost or well-rotted manure into the soil to improve fertility and structure.
3. Timing of Planting
•	Temperature Considerations: Plant tomatoes after the last frost date when soil temperatures consistently measure above 15.5°C (60°F). 
4. Planting Techniques
•	Transplanting Depth: When transplanting seedlings, bury two-thirds of the stem to encourage a stronger root system. This method allows the plant to sprout roots along the buried stem, enhancing stability and drought resistance. 
•	Spacing: Provide adequate spacing between plants to ensure proper air circulation, which helps prevent diseases.
5. Watering Practices
•	Consistent Moisture: Maintain consistent soil moisture, especially during flowering and fruiting stages, to prevent issues like blossom end rot.
•	Watering Method: Use drip irrigation or soaker hoses to deliver water directly to the soil, minimizing foliage wetness and reducing disease risk.
6. Mulching
•	Mulch Application: Apply a layer of mulch around the base of the plants to retain soil moisture, suppress weeds, and regulate soil temperature.
7. Supporting the Plants
•	Staking or Caging: Use stakes, cages, or trellises to support tomato plants, keeping them upright and preventing fruit from contacting the ground.
8. Pruning and Maintenance
•	Pruning: Remove the lower leaves that may touch the soil to improve airflow and reduce the risk of fungal diseases.
•	Monitoring: Regularly inspect plants for signs of pests or diseases and address issues promptly to maintain plant health.
By following these planting guidelines, farmers can establish a strong foundation for their tomato crops, leading to healthier plants and higher yields. """)
    with st.expander("💧 Watering Guide"):
        st.markdown("""
        Proper watering practices are essential for healthy tomato plants and optimal yields. Here's a detailed guide to assist farmers:
1. Watering Frequency
•	Consistent Moisture: Tomato plants require consistent soil moisture. Aim to provide about 1 inch of water per week, adjusting based on rainfall and soil conditions. 
•	Soil Check: Before watering, check soil moisture by inserting your finger about an inch deep. If it feels dry, it's time to water. 
2. Time of Day
•	Morning Watering: Watering in the early morning is ideal, as it reduces evaporation and allows plants to absorb moisture before the day's heat. 
3. Watering Techniques
•	Base Watering: Direct water at the base of the plant to ensure roots receive moisture and to minimize wetting the foliage, which can lead to diseases. 
•	Avoid Overhead Watering: Using sprinklers can wet leaves, increasing the risk of fungal infections.
4. Mulching
•	Moisture Retention: Apply a 2-3 inch layer of organic mulch around the base of tomato plants to retain soil moisture and reduce evaporation. 
5. Soil Drainage
•	Well-Drained Soil: Ensure soil is well-drained to prevent waterlogging, which can lead to root rot. 
6. Signs of Improper Watering
•	Overwatering Indicators: Yellowing leaves, wilting despite damp soil, and mold on the soil surface can signal overwatering. 
•	Underwatering Indicators: Wilting leaves and dry soil suggest the need for more frequent watering.
By following these guidelines, farmers can maintain optimal soil moisture, promoting healthy tomato growth and maximizing yields.""")
    with st.expander("🥕 Essential Nutrients"):
        st.markdown("""
        Ensuring that tomato plants receive the essential nutrients is crucial for their growth, fruit development, and overall health. Here's a detailed guide on the key nutrients required and their roles:
1. Primary Macronutrients
•	Nitrogen (N): Vital for vegetative growth, nitrogen promotes the development of stems and leaves. However, excessive nitrogen can lead to lush foliage with reduced fruit production. 
•	Phosphorus (P): Essential for root development and flowering, phosphorus supports energy transfer within the plant, leading to robust growth and improved fruit set.
•	Potassium (K): Plays a significant role in fruit development, enhancing size, flavor, and disease resistance. Potassium also regulates water uptake and enzyme activation. 
2. Secondary Macronutrients
•	Calcium (Ca): Crucial for cell wall structure, calcium prevents disorders like blossom end rot in tomatoes. It ensures firmness and longevity of the fruit. 
•	Magnesium (Mg): A central component of chlorophyll, magnesium is vital for photosynthesis and enzyme activation.
•	Sulfur (S): Integral to amino acids and proteins, sulfur supports overall plant metabolism.
3. Micronutrients
•	Iron (Fe): Essential for chlorophyll synthesis, iron deficiency can lead to chlorosis, characterized by yellowing leaves.
•	Manganese (Mn): Assists in photosynthesis and nitrogen metabolism.
•	Boron (B): Important for cell wall formation and reproductive development.
•	Zinc (Zn): Involved in hormone production and internode elongation.
•	Copper (Cu): Participates in lignin synthesis and acts as a cofactor for various enzymes.
•	Molybdenum (Mo): Essential for nitrogen fixation and utilization.
4. Nutrient Management Practices
•	Soil Testing: Conducting a soil test before planting is essential to determine existing nutrient levels and pH. This information guides appropriate fertilization strategies.
•	Organic Matter: Incorporating compost or well-rotted manure enhances soil structure and provides a slow-release source of nutrients.
•	Fertilization: Based on soil test results, apply fertilizers to address specific nutrient deficiencies. For instance, adding bone meal can boost phosphorus levels, while potassium sulfate can supply potassium.
•	pH Management: Tomatoes thrive in slightly acidic to neutral soils (pH 6.0-7.0). Adjust soil pH using lime to raise it or sulfur to lower it, ensuring optimal nutrient availability.
By understanding and managing these essential nutrients, farmers can promote vigorous tomato plant growth, enhance fruit quality, and mitigate potential nutrient-related disorders.""")
    with st.expander("🚧 Supporting Tomato Plants"):
        st.markdown("""
        Companion planting is a traditional agricultural practice where specific plants are grown together to enhance growth, improve nutrient uptake, and provide natural pest control. For tomato cultivation, certain companion plants can play a pivotal role in supplementing nutrients and promoting overall plant health. Here's a detailed guide:
1. Benefits of Companion Planting with Tomatoes
•	Enhanced Nutrient Uptake: Some plants improve soil fertility by fixing nutrients or mobilizing them, making them more accessible to tomatoes.
•	Pest and Disease Control: Certain companions repel harmful pests or attract beneficial insects, reducing the need for chemical interventions.
•	Improved Growth and Flavor: Some companion plants can enhance the growth rate and flavor profile of tomatoes.
2. Effective Companion Plants for Tomatoes
•	Basil: Planting basil alongside tomatoes is believed to enhance the flavor of the tomatoes. Additionally, basil acts as a natural repellent against pests like thrips and flies, which can harm tomato plants. 
•	Borage: This herb improves soil health by adding trace minerals, attracting pollinators, and repelling tomato hornworms. It also enhances tomato growth and flavor. 
•	Marigolds: French marigolds release compounds that deter root-knot nematodes, which can damage tomato roots. They also repel other pests, contributing to a healthier tomato crop. 
•	Nasturtiums: Serving as a trap crop, nasturtiums attract aphids and whiteflies away from tomatoes. They also deter other pests and attract beneficial insects like hoverflies, which prey on aphids. 
•	Garlic: Garlic's strong scent helps repel spider mites and other insects that may harm tomato plants. 
3. Implementation Tips
•	Strategic Placement: Plant companion herbs and flowers around tomato beds or intersperse them between tomato plants to maximize benefits.
•	Soil Preparation: Ensure the soil is well-drained and fertile. Adding organic matter can support both tomatoes and their companions.
•	Monitoring: Regularly observe plant health to assess the effectiveness of companion planting and make adjustments as needed.
By integrating these companion plants into tomato cultivation, farmers can naturally enhance nutrient availability, deter pests, and improve overall crop health, leading to more robust yields and sustainable farming practices.""")
    with st.expander("🐞 Pest & Disease Management"):
        st.markdown("""
        **Common Pests & Solutions:**
        - Aphids: Neem oil or garlic spray. 
        - Tomato Hornworms: Handpick and remove. 
        - Whiteflies: Use sticky traps or neem oil. 
        - Spider Mites: Spray with a diluted soap solution. 
        **Common Diseases & Prevention:**
        - Early/Late Blight: Use copper fungicide, remove infected leaves. 
        - Powdery Mildew: Spray with a milk-water solution (1:2 ratio). 
        - Fusarium Wilt: Choose resistant varieties, practice crop rotation. 
        """)
    with st.expander("🐝 Pollination & Flowering"):
        st.markdown("""
       Understanding the processes of flowering and pollination in tomato plants is crucial for achieving optimal fruit production. Here's a comprehensive guide tailored for farmers:
1. Flowering in Tomato Plants
•	Development of Flowers: Tomato plants produce clusters of small, yellow flowers. Each flower has both male (anthers) and female (stigma) reproductive organs, making them self-fertile.
•	Timing: Flowering typically begins 5-7 weeks after planting, depending on the variety and growing conditions.
2. Pollination Mechanism
•	Self-Pollination: Tomato flowers are primarily self-pollinating, meaning they can fertilize themselves without the need for pollen transfer from other flowers.
•	Role of External Factors: While self-pollinating, external agents like wind and insects (e.g., bumblebees) facilitate the movement of pollen from the anthers to the stigma, enhancing pollination efficiency. Gentle shaking of plants can also aid this process. 
3. Factors Affecting Pollination and Fruit Set
•	Temperature: Optimal fruit set occurs when daytime temperatures are between 70°F and 85°F (21°C to 29°C). Temperatures above 90°F (32°C) or below 55°F (13°C) can hinder pollination, leading to blossom drop. 
•	Humidity: Relative humidity around 70% is ideal. High humidity can cause pollen to become sticky, reducing its transferability, while low humidity may cause pollen desiccation. 
•	Watering Practices: Consistent soil moisture is vital. Both overwatering and underwatering can stress plants, negatively impacting flowering and pollination. 
•	Nutrient Management: Excessive nitrogen fertilization encourages vegetative growth at the expense of flowering. Balanced fertilization supports healthy flower development.
4. Enhancing Pollination
•	Manual Assistance: In greenhouse settings or areas with limited insect activity, gently shaking flower clusters or using a small brush to transfer pollen can improve pollination rates. 
•	Attracting Pollinators: Planting nectar-rich flowers near tomato crops can attract pollinators like bees, enhancing natural pollination. 
5. Identifying Successful Pollination
•	Post-Pollination Indicators: After successful pollination, flowers wilt, and the base begins to swell, indicating the initiation of fruit development.
•	Monitoring: Regular inspection of flowers can help identify pollination issues early, allowing for timely interventions.
By closely monitoring and managing these factors, farmers can optimize flowering and pollination in tomato plants, leading to improved fruit set and higher yields.
For a visual guide on identifying successful tomato pollination, you might find this video helpful:
https://youtu.be/sQY6XnvqgjE
        """)  
    with st.expander("🧺 Harvesting & Storage"):
        st.markdown("""
        Proper harvesting and storage of tomatoes are vital to ensure optimal flavor, texture, and shelf life. Here's a comprehensive guide tailored for farmers:
1. Harvesting Tomatoes
•	Maturity Indicators: Harvest tomatoes when they reach full color appropriate to their variety—red, yellow, orange, or purple. The fruit should feel firm yet yield slightly to gentle pressure.
•	Harvesting Technique: Use pruning shears or scissors to cut the stem about half an inch above the fruit to prevent damage.
•	Timing: Pick tomatoes during the cooler parts of the day, such as early morning or late afternoon, to reduce heat stress on the fruit.
2. Post-Harvest Handling
•	Cleaning: Gently brush off any soil or debris. If washing is necessary, ensure tomatoes are thoroughly dried before storage to prevent mold growth.
•	Sorting: Separate damaged or overripe tomatoes from healthy ones to prevent the spread of decay.
3. Storage Practices
•	Ripening Green Tomatoes: For tomatoes harvested before full ripeness, place them in a paper bag or ripening dome, away from direct sunlight, to maintain appropriate humidity levels. This method facilitates even ripening. 
•	Temperature: Store ripe tomatoes at room temperature, ideally between 55°F and 70°F (13°C to 21°C). Avoid refrigeration, as temperatures below 55°F can cause tomatoes to become mushy and lose flavor. 
•	Placement: Arrange tomatoes in a single layer, stem-side down, on a flat surface lined with paper towels. This positioning minimizes moisture loss and bruising. 
4. Long-Term Preservation
•	Canning: Preserve tomatoes by canning them whole, as sauces, salsas, or relishes. This method extends shelf life and maintains flavor. 
•	Drying: Dehydrate tomato slices to create sun-dried tomatoes, which can be stored for extended periods and used in various culinary applications. 
•	Freezing: Although freezing can alter texture, tomatoes can be frozen whole or as purees for use in cooked dishes.
5. Seed Saving
•	Seed Extraction: To save seeds for future planting, select ripe, healthy tomatoes. Extract the seeds and allow them to ferment for several days to remove the gelatinous coating, then dry them thoroughly before storage. 
By adhering to these harvesting and storage practices, farmers can maintain the quality of their tomato crops, reduce post-harvest losses, and ensure a consistent supply for the market or personal use. 
        """)
    with st.expander("Common tomato growth stages"):
        st.markdown("""
        Understanding the growth stages of tomato plants is essential for effective cultivation and management. Here's a detailed overview of the common growth stages:
1. Germination Stage
•	Process: Tomato seeds are typically sown indoors 4 to 6 weeks before the last expected frost. Germination occurs within 6 to 8 days under optimal conditions. 
2. Seedling Stage
•	Development: Following germination, seedlings develop their first true leaves. This stage is crucial for establishing a strong foundation for future growth. 
3. Vegetative Growth Stage
•	Transplanting: Once seedlings have multiple leaves and the risk of frost has passed, they are transplanted outdoors. Soil temperatures should be between 65°F and 70°F (18°C to 21°C) to promote healthy root establishment. 
•	Growth: Plants focus on developing foliage and a robust root system during this phase.
4. Flowering Stage
•	Initiation: Flower clusters begin to form, signaling the plant's readiness to reproduce. Proper nutrient management, especially adequate phosphorus and potassium, supports healthy flowering. 
5. Fruit Set and Development Stage
•	Pollination: Successful pollination leads to fruit formation. Ensuring adequate nutrient supply, particularly calcium, is vital to prevent blossom-end rot and support fruit development. 
6. Fruit Ripening Stage
•	Maturation: Fruits undergo color changes, soften, and develop their characteristic flavors. Reducing nitrogen levels while maintaining potassium and phosphorus supports optimal ripening. 
7. Senescence Stage
•	Conclusion: The plant's growth slows, and it eventually dies after completing its life cycle.
By recognizing and appropriately managing each growth stage, farmers can optimize tomato plant health and maximize yields.
For a visual representation of the tomato growth process, you might find this time-lapse video informative:
https://youtu.be/KwQSjAAIqDo
        """)
# Chatbot UI
elif page == "Chatbot":
    st.header("💬 Tomato Plant Chatbot")
    st.write("Select a category to see available questions.")
    # Dictionary of chatbot questions and responses categorized
    chatbot_data = {
    "General Questions": {
        "What is leaf disease detection?": "Leaf disease detection is the process of identifying plant diseases using AI and machine learning. It analyzes leaf images to determine whether they are healthy or infected.",
        "How does this system work?": "The system uses a deep learning model trained on images of healthy and diseased leaves. When you upload an image, the model analyzes patterns, colors, and textures to classify the disease.",
        "Can I upload any type of plant leaf?": "Our model is trained on specific plant species. If the plant you are testing is outside the dataset, results may not be accurate.",
        "Is this system free to use?": "Yes, the basic disease detection feature is free to use. However, additional features may require a premium subscription in the future.",
        "Does this system work offline?": "Currently, the system requires an internet connection to process and analyze images using cloud-based AI models.",
        "Can this app identify nutrient deficiencies?": "At the moment, the system focuses on disease detection. Future updates may include nutrient deficiency detection.",
    },
    "Image Upload & Detection": {
        "How do I upload an image?": "Click on the 'Upload Leaf Image' button, select an image from your device, and wait for the model to analyze it.",
        "How long does it take to detect a disease?": "The detection process takes just a few seconds after uploading the image.",
        "What should I do if I get an incorrect disease prediction?": "Try uploading a clearer image with good lighting and focus. If the issue persists, consult an expert.",
        "What image formats are supported?": "The system supports JPEG, PNG, and JPG file formats.",
        "What is the maximum file size for image uploads?": "You can upload images up to 20MB in size.",
        "Can I take a live photo for detection?": "Yes, if you are using a mobile device, you can take a live photo and upload it directly for analysis.",
        "Can I upload multiple images at once?": "Currently, the system processes one image at a time. Future updates may support batch processing.",
        "Does image background affect detection?": "Yes, a cluttered background may reduce accuracy. It is recommended to take a close-up of the leaf with a plain background."
    },
    "Accuracy & Confidence": {
        "How accurate is this system?": "The model has an accuracy of X% (replace with actual accuracy). However, accuracy depends on image quality and disease severity.",
        "What does confidence score mean?": "The confidence score represents how sure the model is about its prediction. A higher score means the prediction is more reliable.",
        "Why is accuracy sometimes lower for certain diseases?": "Some diseases have similar visual symptoms, making classification harder. More training data improves accuracy.",
        "Can environmental conditions affect detection accuracy?": "Yes, factors like lighting, image quality, and leaf condition can affect accuracy. Try capturing images in natural daylight.",
        "Will the model improve over time?": "Yes, we continuously update and retrain the model with new data to improve accuracy and detection capabilities.",
        "Can I contribute to improving the AI model?": "Yes! You can contribute images of diseased leaves to help enhance the training dataset."
    },
    "Disease Management & Treatment": {
        "What should I do if my plant has a disease?": "After detection, you will receive a treatment recommendation. You can also consult an expert for further assistance.",
        "Does this app suggest chemical or organic treatments?": "It provides organic treatment options, depending on the disease.",
        "Can this app detect diseases in fruits and flowers?": "Right now, it focuses on leaves, but we plan to expand to fruits and flowers in future updates.",
        "How can I prevent plant diseases?": "Proper watering, soil management, and organic fertilizers help prevent plant diseases. Crop rotation and companion planting also reduce risks.",
        "Where can I find organic solutions for plant diseases?": "The system provides organic treatment suggestions. You can also explore organic pesticides and natural remedies in local nurseries or online stores.",
        "Can I use homemade remedies for plant diseases?": "Yes, some diseases can be treated with homemade solutions like neem oil spray, garlic extract, or baking soda mixtures.",
        "What are some common organic pesticides?": "Neem oil, sulfur spray, copper fungicides, and homemade garlic or chili sprays are effective organic pesticides.",
        "Are there specific fertilizers that help prevent diseases?": "Yes, organic fertilizers rich in potassium and calcium help strengthen plants against infections.",
        "Can this system detect viral, bacterial, and fungal diseases?": "Yes, it can detect a wide range of diseases, including fungal, bacterial, and viral infections, based on leaf symptoms."
    },
    "Technical Support & Future Updates": {
        "What should I do if the app is not working?": "Try refreshing the page, checking your internet connection, or restarting the app. If the issue persists, contact customer support.",
        "Will this app be available on mobile devices?": "Yes, we are working on a mobile-friendly version and plan to launch an app soon.",
        "How often is the disease database updated?": "We regularly update our database with new disease images and solutions to improve accuracy and effectiveness.",
        "Is multi-language support available?": "Currently, the app supports English and Telugu. We plan to add more languages in future updates.",
        "Can I provide feedback on the system?": "Yes! Your feedback is valuable. You can share your thoughts through the feedback section in the app.",
        "Is there a community or forum for users?": "Yes, we are working on creating an online community where users can share experiences and get expert advice.",
        "Will AI-generated recommendations improve over time?": "Yes, as the system learns from new data, treatment recommendations will become more precise and effective.",
        "Can I integrate this system into my own farming tools?": "We are working on an API for third-party integration. Stay tuned for updates!"
    }
}
    # Sidebar category selection
    selected_category = st.selectbox("Choose a Category", list(chatbot_data.keys()))
    # Display questions under selected category
    if selected_category:
        selected_question = st.radio("Select a Question", list(chatbot_data[selected_category].keys()))
        
        if selected_question:
            st.write("**Answer:**", 
            chatbot_data[selected_category][selected_question])