import re
import CrUtil

# # Example input string
file_name = 'dumpfile/all_products.json'
products = CrUtil.load_json_data(file_name)
regex = r'<img[^>]*?\sdata-src\s*=\s*[\'"](.*?)[\'"][^>]*?>'

for product in products:
  new_content = CrUtil.simplify_image(product['content'])
  new_content = CrUtil.clean_enter(new_content)
  new_content = CrUtil.clean_tab(new_content)
  # matches = re.findall(regex, product['content'])
  # Print the matches
  print(new_content.strip())
  # print(matches)


# Example input string
# input_string = '<img decoding="async" class="lazy-load aligncenter size-full wp-image-9926" src="data:image/svg+xml,%3Csvg%20viewBox%3D%220%200%20800%20533%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3C%2Fsvg%3E" data-src="https://thoidaicoffee.vn/wp-content/uploads/2023/04/ban-dong-viner-cook.jpeg" alt="" width="800" height="533" srcset="" data-srcset="https://thoidaicoffee.vn/wp-content/uploads/2023/04/ban-dong-viner-cook.jpeg 800w, https://thoidaicoffee.vn/wp-content/uploads/2023/04/ban-dong-viner-cook-700x466.jpeg 700w, https://thoidaicoffee.vn/wp-content/uploads/2023/04/ban-dong-viner-cook-768x512.jpeg 768w, https://thoidaicoffee.vn/wp-content/uploads/2023/04/ban-dong-viner-cook-600x400.jpeg 600w, https://thoidaicoffee.vn/wp-content/uploads/2023/04/ban-dong-viner-cook-64x43.jpeg 64w" sizes="(max-width: 800px) 100vw, 800px">'

# # Regular expression to match data-src attribute
# regex = r'<img[^>]*?\sdata-src\s*=\s*[\'"](.*?)[\'"][^>]*?>'

# # Extract the data-src attribute value using findall
# matches = re.findall(regex, input_string)

# # Create new string with image tag
# for match in matches:
#     new_string = f'<img src="{match}">'
#     print(new_string)




